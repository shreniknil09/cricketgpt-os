from sqlalchemy.orm import Session

from app.models.innings import Innings
from app.models.over import Over
from app.models.ball import Ball


def get_innings(
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


def get_middle_overs_balls(
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
            Over.over_number >= 7,
            Over.over_number <= 15,
        )
        .order_by(
            Over.over_number.asc(),
            Ball.ball_number.asc(),
        )
        .all()
    )