from sqlalchemy.orm import Session

from app.models.ball import Ball
from app.models.over import Over
from app.models.innings import Innings


def process_extras(
    db: Session,
    ball: Ball,
):
    """
    Handle cricket extras.
    """

    over = (
        db.query(Over)
        .filter(Over.id == ball.over_id)
        .first()
    )

    if over is None:
        return

    innings = (
        db.query(Innings)
        .filter(Innings.id == over.innings_id)
        .first()
    )

    if innings is None:
        return

    # Wide
    if ball.extra_type == "Wide":
        innings.runs += ball.extra_runs

    # No Ball
    elif ball.extra_type == "No Ball":
        innings.runs += ball.extra_runs

    # Bye
    elif ball.extra_type == "Bye":
        innings.runs += ball.extra_runs

    # Leg Bye
    elif ball.extra_type == "Leg Bye":
        innings.runs += ball.extra_runs

    db.commit()
    db.refresh(innings)