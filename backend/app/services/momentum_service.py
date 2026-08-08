from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.match import Match

from app.repositories.momentum_repository import (
    get_current_innings,
    get_recent_balls,
)


def get_momentum(
    db: Session,
    match_id: int,
):
    """
    Calculate current match momentum.

    This is a baseline rule-based momentum model.
    """

    # ---------------------------------
    # Validate Match
    # ---------------------------------

    match = (
        db.query(Match)
        .filter(
            Match.id == match_id,
        )
        .first()
    )

    if match is None:
        raise HTTPException(
            status_code=404,
            detail="Match not found.",
        )

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
    # Get Recent Balls
    # ---------------------------------

    recent_balls = get_recent_balls(
        db,
        innings.id,
    )

    if not recent_balls:
        raise HTTPException(
            status_code=404,
            detail="No ball data found for this innings.",
        )

    # ---------------------------------
    # Calculate Recent Performance
    # ---------------------------------

    recent_runs = 0
    boundary_count = 0
    wicket_count = 0
    legal_balls = 0

    for ball in recent_balls:

        # Runs scored
        recent_runs += ball.runs

        # Boundaries
        if ball.runs in [4, 6]:
            boundary_count += 1

        # Wickets
        if ball.is_wicket:
            wicket_count += 1

        # Legal delivery
        if ball.extra_type not in [
            "Wide",
            "No Ball",
        ]:
            legal_balls += 1

    # ---------------------------------
    # Recent Run Rate
    # ---------------------------------

    if legal_balls > 0:

        recent_run_rate = (
            recent_runs
            / (legal_balls / 6)
        )

    else:

        recent_run_rate = 0.0

    # ---------------------------------
    # Base Momentum
    # ---------------------------------

    momentum_score = 50.0

    # Recent scoring
    if recent_run_rate >= 12:

        momentum_score += 20

    elif recent_run_rate >= 9:

        momentum_score += 12

    elif recent_run_rate >= 7:

        momentum_score += 5

    elif recent_run_rate < 5:

        momentum_score -= 8

    # ---------------------------------
    # Boundary Bonus
    # ---------------------------------

    momentum_score += (
        boundary_count * 4
    )

    # ---------------------------------
    # Wicket Penalty
    # ---------------------------------

    momentum_score -= (
        wicket_count * 15
    )

    # ---------------------------------
    # Clamp Score
    # ---------------------------------

    momentum_score = max(
        0.0,
        min(
            momentum_score,
            100.0,
        ),
    )

    # ---------------------------------
    # Determine Momentum
    # ---------------------------------

    if momentum_score >= 65:

        momentum = "Batting Team Dominating"

        momentum_team_id = (
            innings.batting_team_id
        )

    elif momentum_score <= 35:

        momentum = "Bowling Team Dominating"

        momentum_team_id = (
            innings.bowling_team_id
        )

    else:

        momentum = "Balanced"

        momentum_team_id = (
            innings.batting_team_id
        )

    # ---------------------------------
    # Generate Reason
    # ---------------------------------

    if wicket_count >= 2:

        reason = (
            "Multiple recent wickets have "
            "shifted momentum toward the "
            "bowling team."
        )

    elif (
        boundary_count >= 3
        and recent_run_rate >= 9
    ):

        reason = (
            "Strong recent scoring with "
            "multiple boundaries."
        )

    elif recent_run_rate >= 9:

        reason = (
            "The batting team is scoring "
            "quickly in the recent phase."
        )

    elif recent_run_rate < 5:

        reason = (
            "Recent scoring has been slow, "
            "giving the bowling team control."
        )

    else:

        reason = (
            "Both teams are relatively "
            "balanced in the recent phase."
        )

    # ---------------------------------
    # Return Result
    # ---------------------------------

    return {
        "match_id": match_id,

        "momentum_score": round(
            momentum_score,
            2,
        ),

        "momentum_team_id": (
            momentum_team_id
        ),

        "momentum": momentum,

        "reason": reason,
    }