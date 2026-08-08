from sqlalchemy.orm import Session

from app.models.ball import Ball
from app.models.over import Over
from app.models.innings import Innings


RECENT_BALL_LIMIT = 12


def get_current_innings(
    db: Session,
    match_id: int,
):
    """
    Get the active innings for a match.
    """

    innings = (
        db.query(Innings)
        .filter(
            Innings.match_id == match_id,
            Innings.innings_number == 2,
        )
        .first()
    )

    if innings is not None:
        return innings

    return (
        db.query(Innings)
        .filter(
            Innings.match_id == match_id,
            Innings.innings_number == 1,
        )
        .first()
    )


def get_recent_balls(
    db: Session,
    innings_id: int,
):
    """
    Get the most recent deliveries
    from the current innings.
    """

    balls = (
        db.query(Ball)
        .join(
            Over,
            Ball.over_id == Over.id,
        )
        .filter(
            Over.innings_id == innings_id,
        )
        .order_by(
            Over.over_number.desc(),
            Ball.ball_number.desc(),
        )
        .limit(RECENT_BALL_LIMIT)
        .all()
    )

    return list(reversed(balls))