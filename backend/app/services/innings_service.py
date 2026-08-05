from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.match import Match
from app.repositories.innings_repository import (
    create_innings,
    get_all_innings,
    get_innings_by_id,
    get_match_innings,
)


def get_innings(db: Session):
    return get_all_innings(db)


def get_single_innings(
    db: Session,
    innings_id: int,
):
    innings = get_innings_by_id(db, innings_id)

    if innings is None:
        raise HTTPException(
            status_code=404,
            detail="Innings not found.",
        )

    return innings


def add_innings(
    db: Session,
    innings,
):
    # Rule 1: Match must exist
    match = (
        db.query(Match)
        .filter(Match.id == innings.match_id)
        .first()
    )

    if match is None:
        raise HTTPException(
            status_code=404,
            detail="Match not found.",
        )

    # Rule 2: Maximum 2 innings per match
    existing_innings = get_match_innings(
        db,
        innings.match_id,
    )

    if len(existing_innings) >= 2:
        raise HTTPException(
            status_code=400,
            detail="Only two innings are allowed per match.",
        )

    # Rule 3: Innings number must be 1 or 2
    if innings.innings_number not in [1, 2]:
        raise HTTPException(
            status_code=400,
            detail="Innings number must be either 1 or 2.",
        )

    # Rule 4: Batting and bowling teams cannot be the same
    if innings.batting_team_id == innings.bowling_team_id:
        raise HTTPException(
            status_code=400,
            detail="Batting and bowling teams cannot be the same.",
        )

    # Rule 5: Teams must belong to the match
    valid_teams = [match.team1_id, match.team2_id]

    if (
        innings.batting_team_id not in valid_teams
        or innings.bowling_team_id not in valid_teams
    ):
        raise HTTPException(
            status_code=400,
            detail="Selected teams are not part of this match.",
        )

    return create_innings(db, innings)