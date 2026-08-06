from sqlalchemy.orm import Session

from app.models.ball import Ball
from app.models.over import Over


def process_over(
    db: Session,
    ball: Ball,
):
    """
    Complete an over after 6 legal deliveries.
    """

    over = (
        db.query(Over)
        .filter(Over.id == ball.over_id)
        .first()
    )

    if over is None:
        return

    # Count only legal balls
    legal_balls = (
        db.query(Ball)
        .filter(
            Ball.over_id == over.id,
            Ball.extra_type.notin_(["Wide", "No Ball"]),
        )
        .count()
    )

    if legal_balls >= 6:
        over.status = "Completed"

        db.commit()
        db.refresh(over)