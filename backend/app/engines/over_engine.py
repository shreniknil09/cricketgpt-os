from sqlalchemy.orm import Session

from app.models.ball import Ball
from app.models.over import Over
from app.models.innings import Innings


def process_over(
    db: Session,
    ball: Ball,
):
    """
    Complete an over after 6 legal deliveries.

    Also updates the innings over count.
    """

    # ---------------------------------
    # Find Over
    # ---------------------------------

    over = (
        db.query(Over)
        .filter(
            Over.id == ball.over_id,
        )
        .first()
    )

    if over is None:
        return

    # ---------------------------------
    # Find Innings
    # ---------------------------------

    innings = (
        db.query(Innings)
        .filter(
            Innings.id == over.innings_id,
        )
        .first()
    )

    if innings is None:
        return

    # ---------------------------------
    # Count Legal Deliveries
    # ---------------------------------

    legal_balls = (
        db.query(Ball)
        .filter(
            Ball.over_id == over.id,
            Ball.extra_type.notin_(
                ["Wide", "No Ball"]
            ),
        )
        .count()
    )

    # ---------------------------------
    # Complete Over
    # ---------------------------------

    if (
        legal_balls >= 6
        and over.status != "Completed"
    ):

        over.status = "Completed"

        # Increment completed overs
        innings.overs += 1

    # ---------------------------------
    # Save Changes
    # ---------------------------------

    db.commit()
    db.refresh(over)
    db.refresh(innings)