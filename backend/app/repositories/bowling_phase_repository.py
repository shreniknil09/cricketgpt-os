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
            Innings.match_id == match_id
        )
        .order_by(
            Innings.id.desc()
        )
        .first()
    )


def get_phase_balls(
    db: Session,
    innings_id: int,
    min_over: int,
    max_over: int,
):
    return (
        db.query(
            Ball,
            Over.over_number,
        )
        .join(
            Over,
            Ball.over_id == Over.id,
        )
        .filter(
            Over.innings_id == innings_id,
            Over.over_number >= min_over,
            Over.over_number <= max_over,
        )
        .order_by(
            Over.over_number.asc(),
            Ball.ball_number.asc(),
        )
        .all()
    )