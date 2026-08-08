from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.match import Match

from app.repositories.win_probability_repository import (
    get_current_innings,
    get_first_innings,
)


def get_win_probability(
    db: Session,
    match_id: int,
):
    """
    Calculate a basic win probability
    for the chasing team.
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
    # Get First Innings
    # ---------------------------------

    first_innings = get_first_innings(
        db,
        match_id,
    )

    if first_innings is None:
        raise HTTPException(
            status_code=404,
            detail="First innings not found.",
        )

    # ---------------------------------
    # Get Second Innings
    # ---------------------------------

    second_innings = get_current_innings(
        db,
        match_id,
    )

    if second_innings is None:
        raise HTTPException(
            status_code=404,
            detail="Second innings not found.",
        )

    # ---------------------------------
    # Calculate Target
    # ---------------------------------

    target = first_innings.runs + 1

    runs_required = max(
        target - second_innings.runs,
        0,
    )

    # ---------------------------------
    # Calculate Balls Remaining
    # ---------------------------------

    total_balls = 20 * 6

    balls_used = (
        second_innings.overs * 6
        + second_innings.balls
    )

    balls_remaining = max(
        total_balls - balls_used,
        0,
    )

    # ---------------------------------
    # Calculate Wickets Remaining
    # ---------------------------------

    wickets_remaining = max(
        10 - second_innings.wickets,
        0,
    )

    # ---------------------------------
    # Match Already Won
    # ---------------------------------

    if runs_required == 0:

        batting_probability = 100.0
        bowling_probability = 0.0

    # ---------------------------------
    # Match Already Completed
    # ---------------------------------

    elif (
        second_innings.wickets >= 10
        or balls_remaining == 0
    ):

        if second_innings.runs >= target:

            batting_probability = 100.0
            bowling_probability = 0.0

        else:

            batting_probability = 0.0
            bowling_probability = 100.0

    # ---------------------------------
    # Probability Calculation
    # ---------------------------------

    else:

        # Required run rate
        required_run_rate = (
            runs_required
            / (balls_remaining / 6)
        )

        # Base probability
        batting_probability = 50.0

        # Easier chase
        if required_run_rate <= 6:

            batting_probability += 25

        elif required_run_rate <= 8:

            batting_probability += 15

        elif required_run_rate <= 10:

            batting_probability += 5

        elif required_run_rate <= 12:

            batting_probability -= 10

        else:

            batting_probability -= 25

        # Wicket factor
        batting_probability += (
            wickets_remaining - 5
        ) * 2

        # Clamp probability
        batting_probability = max(
            1.0,
            min(
                batting_probability,
                99.0,
            ),
        )

        bowling_probability = (
            100.0 - batting_probability
        )

    # ---------------------------------
    # Return Result
    # ---------------------------------

    return {
        "match_id": match_id,
        "batting_team_id": (
            second_innings.batting_team_id
        ),
        "bowling_team_id": (
            second_innings.bowling_team_id
        ),
        "batting_team_probability": round(
            batting_probability,
            2,
        ),
        "bowling_team_probability": round(
            bowling_probability,
            2,
        ),
        "runs_required": runs_required,
        "balls_remaining": balls_remaining,
        "wickets_remaining": wickets_remaining,
    }