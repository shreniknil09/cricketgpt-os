from sqlalchemy.orm import Session

from app.models.ball import Ball
from app.models.over import Over


def get_innings_wickets(
    db: Session,
    innings_id: int,
):
    """
    Get all wicket deliveries for an innings.
    """

    return (
        db.query(Ball, Over)
        .join(
            Over,
            Ball.over_id == Over.id,
        )
        .filter(
            Over.innings_id == innings_id,
            Ball.is_wicket.is_(True),
        )
        .order_by(
            Over.over_number,
            Ball.ball_number,
        )
        .all()
    )