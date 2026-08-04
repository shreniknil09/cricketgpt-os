from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.playing_xi_repository import (
    batting_position_exists,
    captain_exists,
    count_players_in_team,
    create_playing_xi,
    get_all_playing_xi,
    get_playing_xi_by_id,
    player_belongs_to_team,
    player_exists_in_match,
    wicketkeeper_exists,
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

    # Rule 1
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

    # Rule 2
    if player_exists_in_match(
        db,
        player.match_id,
        player.player_id,
    ):
        raise HTTPException(
            status_code=400,
            detail="This player has already been selected for this match.",
        )

    # Rule 3
    if player.is_captain:
        if captain_exists(
            db,
            player.match_id,
            player.team_id,
        ):
            raise HTTPException(
                status_code=400,
                detail="This team already has a captain.",
            )

    # Rule 4
    if player.is_wicketkeeper:
        if wicketkeeper_exists(
            db,
            player.match_id,
            player.team_id,
        ):
            raise HTTPException(
                status_code=400,
                detail="This team already has a wicketkeeper.",
            )

    # Rule 5
    if player.batting_position < 1 or player.batting_position > 11:
        raise HTTPException(
            status_code=400,
            detail="Batting position must be between 1 and 11.",
        )

    # Rule 6
    if batting_position_exists(
        db,
        player.match_id,
        player.team_id,
        player.batting_position,
    ):
        raise HTTPException(
            status_code=400,
            detail="This batting position has already been assigned.",
        )

     # Rule 7: Player must belong to selected team
    if not player_belongs_to_team(
        db,
        player.player_id,
        player.team_id,
    ):
        raise HTTPException(
            status_code=400,
            detail="Selected player does not belong to this team.",
        )

    return create_playing_xi(db, player)