from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.playing_xi_repository import (
    count_players_in_team,
    create_playing_xi,
    get_all_playing_xi,
    get_playing_xi_by_id,
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

    return create_playing_xi(db, player)