from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.toss_repository import (
    create_toss,
    get_all_tosses,
    get_toss_by_id,
    get_toss_by_match,
)
from app.models.match import Match


def get_tosses(db: Session):
    return get_all_tosses(db)


def get_toss(db: Session, toss_id: int):
    toss = get_toss_by_id(db, toss_id)

    if toss is None:
        raise HTTPException(
            status_code=404,
            detail="Toss not found.",
        )

    return toss


def add_toss(db: Session, toss):

    # Rule 1: One toss per match
    existing_toss = get_toss_by_match(db, toss.match_id)

    if existing_toss:
        raise HTTPException(
            status_code=400,
            detail="Toss already exists for this match.",
        )

    # Rule 2: Match must exist
    match = (
        db.query(Match)
        .filter(Match.id == toss.match_id)
        .first()
    )

    if match is None:
        raise HTTPException(
            status_code=404,
            detail="Match not found.",
        )

    # Rule 3: Winning team must be one of the two teams
    if toss.winning_team_id not in [match.team1_id, match.team2_id]:
        raise HTTPException(
            status_code=400,
            detail="Winning team is not part of this match.",
        )

    # Rule 4: Decision must be Bat or Bowl
    if toss.decision not in ["Bat", "Bowl"]:
        raise HTTPException(
            status_code=400,
            detail="Decision must be 'Bat' or 'Bowl'.",
        )

    # Rule 5: Batting and bowling teams must be different
    if toss.batting_team_id == toss.bowling_team_id:
        raise HTTPException(
            status_code=400,
            detail="Batting and bowling teams cannot be the same.",
        )

    return create_toss(db, toss)