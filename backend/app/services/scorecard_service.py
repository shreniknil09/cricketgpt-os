from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.scorecard_repository import (
    get_batting_scorecard,
    get_bowling_scorecard,
    get_innings_score,
)


def get_match_scorecard(
    db: Session,
    match_id: int,
):
    innings = get_innings_score(
        db,
        match_id,
    )

    if innings is None:
        raise HTTPException(
            status_code=404,
            detail="Match not found.",
        )

    batting = get_batting_scorecard(
        db,
        match_id,
    )

    bowling = get_bowling_scorecard(
        db,
        match_id,
    )

    return {
        "innings": innings,
        "batting": batting,
        "bowling": bowling,
    }