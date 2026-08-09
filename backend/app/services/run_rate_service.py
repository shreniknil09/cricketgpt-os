from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.run_rate_repository import (
    get_current_innings,
    get_innings_balls,
)


RECENT_BALL_LIMIT = 12


def get_run_rate(
    db: Session,
    match_id: int,
):
    """
    Calculate current and recent run rate.
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
    # Total Runs
    # ---------------------------------

    total_runs = sum(
        ball.runs or 0
        for ball in balls
    )

    # ---------------------------------
    # Legal Balls
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
    # Current Run Rate
    # ---------------------------------

    current_run_rate = (
        total_runs
        / (legal_balls / 6)
    )

    # ---------------------------------
    # Recent Balls
    # ---------------------------------

    recent_balls = balls[
        -RECENT_BALL_LIMIT:
    ]

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

    # ---------------------------------
    # Recent Run Rate
    # ---------------------------------

    if recent_legal_balls > 0:

        recent_run_rate = (
            recent_runs
            / (recent_legal_balls / 6)
        )

    else:

        recent_run_rate = current_run_rate

    # ---------------------------------
    # Run Rate Change
    # ---------------------------------

    run_rate_change = (
        recent_run_rate
        - current_run_rate
    )

    # ---------------------------------
    # Determine Trend
    # ---------------------------------

    if run_rate_change >= 1.5:

        trend = "Strongly Accelerating"

    elif run_rate_change >= 0.5:

        trend = "Accelerating"

    elif run_rate_change <= -1.5:

        trend = "Strongly Declining"

    elif run_rate_change <= -0.5:

        trend = "Declining"

    else:

        trend = "Stable"

    # ---------------------------------
    # Current Overs
    # ---------------------------------

    completed_overs = (
        legal_balls // 6
    )

    remaining_balls = (
        legal_balls % 6
    )

    current_overs = (
        completed_overs
        + remaining_balls / 10
    )

    # ---------------------------------
    # Return
    # ---------------------------------

    return {
        "match_id": match_id,

        "innings_id": innings.id,

        "total_runs": int(
            total_runs
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

        "recent_run_rate": round(
            recent_run_rate,
            2,
        ),

        "run_rate_change": round(
            run_rate_change,
            2,
        ),

        "trend": trend,
    }