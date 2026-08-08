from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.venue_analysis_repository import (
    get_venue_team_matches,
)


def get_venue_analysis(
    db: Session,
    team_id: int,
    venue_id: int,
):
    """
    Analyze a team's historical performance
    at a specific venue.
    """

    matches = get_venue_team_matches(
        db,
        team_id,
        venue_id,
    )

    if not matches:
        raise HTTPException(
            status_code=404,
            detail="No completed matches found for this team at this venue.",
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
    # Venue Rating
    # ---------------------------------

    venue_rating = win_rate

    # ---------------------------------
    # Venue Status
    # ---------------------------------

    if venue_rating >= 80:

        venue_status = "Excellent"

    elif venue_rating >= 60:

        venue_status = "Good"

    elif venue_rating >= 40:

        venue_status = "Average"

    elif venue_rating >= 20:

        venue_status = "Poor"

    else:

        venue_status = "Very Poor"

    # ---------------------------------
    # Return
    # ---------------------------------

    return {
        "team_id": team_id,

        "venue_id": venue_id,

        "matches": total_matches,

        "wins": wins,

        "losses": losses,

        "win_rate": round(
            win_rate,
            2,
        ),

        "venue_rating": round(
            venue_rating,
            2,
        ),

        "venue_status": venue_status,
    }