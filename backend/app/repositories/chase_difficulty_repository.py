from sqlalchemy.orm import Session

from app.models.match import Match
from app.models.innings import Innings
from app.models.over import Over
from app.models.ball import Ball


def get_match(
    db: Session,
    match_id: int,
):
    return (
        db.query(Match)
        .filter(
            Match.id == match_id,
        )
        .first()
    )


def get_current_innings(
    db: Session,
    match_id: int,
):
    return (
        db.query(Innings)
        .filter(
            Innings.match_id == match_id,
        )
        .order_by(
            Innings.id.desc(),
        )
        .first()
    )


def get_innings_balls(
    db: Session,
    innings_id: int,
):
    return (
        db.query(Ball)
        .join(
            Over,
            Ball.over_id == Over.id,
        )
        .filter(
            Over.innings_id == innings_id,
        )
        .order_by(
            Over.over_number.asc(),
            Ball.ball_number.asc(),
        )
        .all()
    )