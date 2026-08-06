from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.live_score_repository import (
    get_live_score,
)


def get_match_live_score(
    db: Session,
    match_id: int,
):
    """
    Returns the current live score
    for a match.
    """

    innings = get_live_score(
        db,
        match_id,
    )

    if innings is None:
        raise HTTPException(
            status_code=404,
            detail="No active innings found for this match.",
        )

    return innings