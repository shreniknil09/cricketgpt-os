from sqlalchemy.orm import Session

from app.models.player import Player


def get_all_players(db: Session):
    return db.query(Player).all()


def create_player(db: Session, player):
    new_player = Player(
        name=player.name,
        batting_style=player.batting_style,
        bowling_style=player.bowling_style,
        role=player.role,
        team_id=player.team_id,
    )

    db.add(new_player)
    db.commit()
    db.refresh(new_player)

    return new_player