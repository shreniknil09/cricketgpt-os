from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.match import Match
from app.models.player import Player

from app.repositories.player_match_stats_repository import (
    create_player_stats,
    get_all_player_stats,
    get_match_player_stats,
    get_player_stats_by_id,
)


def get_player_stats(db: Session):
    return get_all_player_stats(db)


def get_single_player_stats(
    db: Session,
    stats_id: int,
):
    stats = get_player_stats_by_id(
        db,
        stats_id,
    )

    if stats is None:
        raise HTTPException(
            status_code=404,
            detail="Player statistics not found.",
        )

    return stats


def add_player_stats(
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

    existing = get_match_player_stats(
        db,
        stats.match_id,
        stats.player_id,
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Statistics already exist for this player in this match.",
        )

    return create_player_stats(
        db,
        stats,
    )