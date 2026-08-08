from sqlalchemy.orm import Session

from app.models.ball import Ball
from app.models.over import Over


def get_innings_balls(
    db: Session,
    innings_id: int,
):
    """
    Get all balls belonging to an innings.

    Balls are retrieved through the Over table.
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
            Over.over_number,
            Ball.ball_number,
        )
        .all()
    )