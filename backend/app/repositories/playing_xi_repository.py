from sqlalchemy.orm import Session

from app.models.playing_xi import PlayingXI


def get_all_playing_xi(db: Session):
    return db.query(PlayingXI).all()


def get_playing_xi_by_id(db: Session, playing_xi_id: int):
    return (
        db.query(PlayingXI)
        .filter(PlayingXI.id == playing_xi_id)
        .first()
    )


def count_players_in_team(
    db: Session,
    match_id: int,
    team_id: int,
):
    return (
        db.query(PlayingXI)
        .filter(
            PlayingXI.match_id == match_id,
            PlayingXI.team_id == team_id,
        )
        .count()
    )


def player_exists_in_match(
    db: Session,
    match_id: int,
    player_id: int,
):
    return (
        db.query(PlayingXI)
        .filter(
            PlayingXI.match_id == match_id,
            PlayingXI.player_id == player_id,
        )
        .first()
    )


def create_playing_xi(db: Session, player):
    new_player = PlayingXI(
        match_id=player.match_id,
        team_id=player.team_id,
        player_id=player.player_id,
        batting_position=player.batting_position,
        is_captain=player.is_captain,
        is_wicketkeeper=player.is_wicketkeeper,
    )

    db.add(new_player)
    db.commit()
    db.refresh(new_player)

    return new_player