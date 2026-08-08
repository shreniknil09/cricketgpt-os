from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.score_prediction_repository import (
    get_current_innings,
    get_innings_balls,
)


MAX_OVERS = 20


def get_score_prediction(
    db: Session,
    match_id: int,
):
    """
    Predict the final score of the current innings.

    Version 1 uses current run rate and recent scoring
    as a transparent rule-based baseline.
    """

    # ---------------------------------
    # Get Current Innings
    # ---------------------------------

    innings = get_current_innings(
        db,
        match_id,
    )

    if innings is None:
        raise HTTPException(
            status_code=404,
            detail="No innings found for this match.",
        )

    # ---------------------------------
    # Get Balls
    # ---------------------------------

    balls = get_innings_balls(
        db,
        innings.id,
    )

    if not balls:
        raise HTTPException(
            status_code=404,
            detail="No ball data found for this innings.",
        )

    # ---------------------------------
    # Calculate Current Score
    # ---------------------------------

    total_runs = sum(
        ball.runs or 0
        for ball in balls
    )

    # ---------------------------------
    # Calculate Wickets
    # ---------------------------------

    wickets = sum(
        1
        for ball in balls
        if ball.is_wicket
    )

    # ---------------------------------
    # Calculate Legal Balls
    # ---------------------------------

    legal_balls = sum(
        1
        for ball in balls
        if ball.extra_type not in [
            "Wide",
            "No Ball",
        ]
    )

    if legal_balls == 0:
        raise HTTPException(
            status_code=400,
            detail="No legal deliveries available.",
        )

    # ---------------------------------
    # Current Overs
    # ---------------------------------

    completed_overs = (
        legal_balls // 6
    )

    remaining_balls_in_over = (
        legal_balls % 6
    )

    current_overs = (
        completed_overs
        + (
            remaining_balls_in_over
            / 10
        )
    )

    # ---------------------------------
    # Current Run Rate
    # ---------------------------------

    current_run_rate = (
        total_runs
        / (legal_balls / 6)
    )

    # ---------------------------------
    # Recent Run Rate
    # ---------------------------------

    recent_balls = balls[-12:]

    recent_runs = sum(
        ball.runs or 0
        for ball in recent_balls
    )

    recent_legal_balls = sum(
        1
        for ball in recent_balls
        if ball.extra_type not in [
            "Wide",
            "No Ball",
        ]
    )

    if recent_legal_balls > 0:

        recent_run_rate = (
            recent_runs
            / (recent_legal_balls / 6)
        )

    else:

        recent_run_rate = (
            current_run_rate
        )

    # ---------------------------------
    # Weighted Run Rate
    # ---------------------------------

    # Give recent scoring slightly more
    # importance than the full innings rate.

    weighted_run_rate = (
        current_run_rate * 0.60
        + recent_run_rate * 0.40
    )

    # ---------------------------------
    # Remaining Overs
    # ---------------------------------

    remaining_legal_balls = max(
        0,
        (MAX_OVERS * 6) - legal_balls,
    )

    remaining_overs = (
        remaining_legal_balls / 6
    )

    # ---------------------------------
    # Wicket Adjustment
    # ---------------------------------

    if wickets >= 7:

        weighted_run_rate *= 0.80

    elif wickets >= 5:

        weighted_run_rate *= 0.90

    elif wickets >= 3:

        weighted_run_rate *= 0.95

    # ---------------------------------
    # Project Remaining Runs
    # ---------------------------------

    projected_remaining_runs = (
        weighted_run_rate
        * remaining_overs
    )

    # ---------------------------------
    # Predicted Final Score
    # ---------------------------------

    predicted_score = (
        total_runs
        + projected_remaining_runs
    )

    # ---------------------------------
    # Prediction Range
    # ---------------------------------

    lower_prediction = (
        predicted_score * 0.95
    )

    upper_prediction = (
        predicted_score * 1.05
    )

    # ---------------------------------
    # Don't allow prediction below
    # current score.
    # ---------------------------------

    predicted_score = max(
        predicted_score,
        total_runs,
    )

    lower_prediction = max(
        lower_prediction,
        total_runs,
    )

    upper_prediction = max(
        upper_prediction,
        predicted_score,
    )

    # ---------------------------------
    # If innings is already complete
    # ---------------------------------

    if legal_balls >= MAX_OVERS * 6:

        predicted_score = total_runs

        lower_prediction = total_runs

        upper_prediction = total_runs

    # ---------------------------------
    # Return
    # ---------------------------------

    return {
        "match_id": match_id,

        "innings_id": innings.id,

        "current_score": int(
            total_runs
        ),

        "current_wickets": int(
            wickets
        ),

        "legal_balls": int(
            legal_balls
        ),

        "current_overs": round(
            current_overs,
            1,
        ),

        "current_run_rate": round(
            current_run_rate,
            2,
        ),

        "predicted_score": int(
            round(predicted_score)
        ),

        "lower_prediction": int(
            round(lower_prediction)
        ),

        "upper_prediction": int(
            round(upper_prediction)
        ),
    }