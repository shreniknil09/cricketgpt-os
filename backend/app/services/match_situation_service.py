from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.match import Match

from app.repositories.match_situation_repository import (
    get_current_innings,
    get_first_innings,
)


MAX_OVERS = 20
BALLS_PER_OVER = 6
MAX_WICKETS = 10


def get_match_situation(
    db: Session,
    match_id: int,
):
    """
    Analyze the current situation of a cricket match.
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
    # Get First Innings
    # ---------------------------------

    first_innings = get_first_innings(
        db,
        match_id,
    )

    # ---------------------------------
    # Current Score
    # ---------------------------------

    runs = innings.runs
    wickets = innings.wickets

    overs = innings.overs
    balls = innings.balls

    # ---------------------------------
    # Legal Balls Played
    # ---------------------------------

    balls_played = (
        overs * BALLS_PER_OVER
        + balls
    )

    # ---------------------------------
    # Current Run Rate
    # ---------------------------------

    if balls_played > 0:

        current_run_rate = (
            runs / (balls_played / 6)
        )

    else:

        current_run_rate = 0.0

    # ---------------------------------
    # Default Chase Values
    # ---------------------------------

    runs_required = 0
    balls_remaining = (
        MAX_OVERS * BALLS_PER_OVER
        - balls_played
    )

    wickets_remaining = (
        MAX_WICKETS - wickets
    )

    required_run_rate = 0.0

    # ---------------------------------
    # Chasing Situation
    # ---------------------------------

    if (
        innings.innings_number == 2
        and first_innings is not None
    ):

        target = first_innings.runs + 1

        runs_required = max(
            target - runs,
            0,
        )

        balls_remaining = max(
            balls_remaining,
            0,
        )

        wickets_remaining = max(
            wickets_remaining,
            0,
        )

        if (
            runs_required > 0
            and balls_remaining > 0
        ):

            required_run_rate = (
                runs_required
                / (balls_remaining / 6)
            )

    # ---------------------------------
    # Pressure Level
    # ---------------------------------

    pressure_level = "Low"

    if required_run_rate > 0:

        if required_run_rate <= 6:
            pressure_level = "Low"

        elif required_run_rate <= 9:
            pressure_level = "Medium"

        elif required_run_rate <= 12:
            pressure_level = "High"

        else:
            pressure_level = "Extreme"

    # ---------------------------------
    # Situation Description
    # ---------------------------------

    if innings.innings_number == 1:

        situation = "Setting the target"

    elif runs_required == 0:

        situation = "Target achieved"

    elif wickets_remaining <= 2:

        situation = "Chasing with very few wickets remaining"

    elif required_run_rate > 12:

        situation = "Chasing aggressively under severe pressure"

    elif required_run_rate > 9:

        situation = "Chasing under pressure"

    elif required_run_rate <= 6:

        situation = "Comfortable chase"

    else:

        situation = "Balanced chase"

    # ---------------------------------
    # Return Situation
    # ---------------------------------

    return {
        "match_id": match_id,

        "batting_team_id": (
            innings.batting_team_id
        ),

        "bowling_team_id": (
            innings.bowling_team_id
        ),

        "runs": runs,
        "wickets": wickets,

        "overs": overs,
        "balls": balls,

        "current_run_rate": round(
            current_run_rate,
            2,
        ),

        "runs_required": runs_required,

        "balls_remaining": balls_remaining,

        "required_run_rate": round(
            required_run_rate,
            2,
        ),

        "wickets_remaining": wickets_remaining,

        "pressure_level": pressure_level,

        "situation": situation,
    }