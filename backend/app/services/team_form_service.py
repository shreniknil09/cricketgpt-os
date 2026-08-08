from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.team_form_repository import (
    get_recent_team_matches,
)


def get_team_form(
    db: Session,
    team_id: int,
):
    """
    Calculate recent team form.
    """

    matches = get_recent_team_matches(
        db,
        team_id,
    )

    if not matches:
        raise HTTPException(
            status_code=404,
            detail="No completed matches found for this team.",
        )

    # ---------------------------------
    # Calculate Wins / Losses
    # ---------------------------------

    wins = 0
    losses = 0

    for match in matches:

        if match.winner_id == team_id:

            wins += 1

        elif (
            match.winner_id is not None
            and match.winner_id != team_id
        ):

            losses += 1

    # ---------------------------------
    # Win Rate
    # ---------------------------------

    total_matches = len(matches)

    win_rate = (
        wins
        / total_matches
        * 100
    )

    # ---------------------------------
    # Form Rating
    # ---------------------------------

    form_rating = win_rate

    # ---------------------------------
    # Form Status
    # ---------------------------------

    if form_rating >= 80:

        form_status = "Excellent"

    elif form_rating >= 60:

        form_status = "Good"

    elif form_rating >= 40:

        form_status = "Average"

    elif form_rating >= 20:

        form_status = "Poor"

    else:

        form_status = "Very Poor"

    # ---------------------------------
    # Return
    # ---------------------------------

    return {
        "team_id": team_id,

        "matches": total_matches,

        "wins": wins,

        "losses": losses,

        "win_rate": round(
            win_rate,
            2,
        ),

        "form_rating": round(
            form_rating,
            2,
        ),

        "form_status": form_status,
    }