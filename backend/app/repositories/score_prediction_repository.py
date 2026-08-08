from sqlalchemy.orm import Session

from app.models.innings import Innings
from app.models.over import Over
from app.models.ball import Ball


def get_current_innings(
    db: Session,
    match_id: int,
):
    """
    Get the latest innings for the match.
    """

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


def get_innings_overs(
    db: Session,
    innings_id: int,
):
    """
    Get all overs belonging to an innings.
    """

    return (
        db.query(Over)
        .filter(
            Over.innings_id == innings_id,
        )
        .order_by(
            Over.over_number.asc(),
        )
        .all()
    )


def get_innings_balls(
    db: Session,
    innings_id: int,
):
    """
    Get all balls belonging to an innings.
    """

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