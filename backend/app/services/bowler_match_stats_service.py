from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.match import Match
from app.models.player import Player

from app.repositories.bowler_match_stats_repository import (
    create_bowler_stats,
    get_all_bowler_stats,
    get_bowler_stats_by_id,
    get_match_bowler_stats,
)


def get_bowler_stats(db: Session):
    return get_all_bowler_stats(db)


def get_single_bowler_stats(
    db: Session,
    stats_id: int,
):
    stats = get_bowler_stats_by_id(
        db,
        stats_id,
    )

    if stats is None:
        raise HTTPException(
            status_code=404,
            detail="Bowler statistics not found.",
        )

    return stats


def add_bowler_stats(
    db: Session,
    stats,
):
    match = (
        db.query(Match)
        .filter(Match.id == stats.match_id)
        .first()
    )

    if match is None:
        raise HTTPException(
            status_code=404,
            detail="Match not found.",
        )

    player = (
        db.query(Player)
        .filter(Player.id == stats.player_id)
        .first()
    )

    if player is None:
        raise HTTPException(
            status_code=404,
            detail="Player not found.",
        )

    existing = get_match_bowler_stats(
        db,
        stats.match_id,
        stats.player_id,
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Bowler statistics already exist for this player in this match.",
        )

    return create_bowler_stats(
        db,
        stats,
    )