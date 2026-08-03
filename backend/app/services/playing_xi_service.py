from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.playing_xi_repository import (
    count_players_in_team,
    create_playing_xi,
    get_all_playing_xi,
    get_playing_xi_by_id,
    player_exists_in_match,
)


def get_playing_xi(db: Session):
    return get_all_playing_xi(db)


def get_player(db: Session, playing_xi_id: int):
    player = get_playing_xi_by_id(db, playing_xi_id)

    if player is None:
        raise HTTPException(
            status_code=404,
            detail="Player not found in Playing XI",
        )

    return player


def add_player(db: Session, player):

    # Rule 1: Maximum 11 players
    total_players = count_players_in_team(
        db,
        player.match_id,
        player.team_id,
    )

    if total_players >= 11:
        raise HTTPException(
            status_code=400,
            detail="A team can only have 11 players in the Playing XI.",
        )

    # Rule 2: No duplicate players
    existing_player = player_exists_in_match(
        db,
        player.match_id,
        player.player_id,
    )

    if existing_player:
        raise HTTPException(
            status_code=400,
            detail="This player has already been selected for this match.",
        )

    return create_playing_xi(db, player)