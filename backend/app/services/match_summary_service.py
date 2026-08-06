from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.match_summary_repository import (
    get_match,
    get_match_innings,
)


def get_summary(
    db: Session,
    match_id: int,
):
    match = get_match(
        db,
        match_id,
    )

    if match is None:
        raise HTTPException(
            status_code=404,
            detail="Match not found.",
        )

    innings = get_match_innings(
        db,
        match_id,
    )

    return {
        "match_id": match.id,
        "team1_id": match.team1_id,
        "team2_id": match.team2_id,
        "venue_id": match.venue_id,
        "tournament_id": match.tournament_id,
        "status": match.status,
        "innings": innings,
    }