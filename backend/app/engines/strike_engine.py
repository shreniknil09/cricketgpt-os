from sqlalchemy.orm import Session

from app.models.ball import Ball
from app.models.over import Over
from app.models.innings import Innings


def rotate_strike(
    db: Session,
    ball: Ball,
):
    """
    Rotate strike after odd runs.
    """

    # Get Over
    over = (
        db.query(Over)
        .filter(Over.id == ball.over_id)
        .first()
    )

    if over is None:
        return

    # Get Innings
    innings = (
        db.query(Innings)
        .filter(Innings.id == over.innings_id)
        .first()
    )

    if innings is None:
        return

    # Rotate strike only on odd runs
    if (
        ball.extra_type is None
        and ball.runs % 2 == 1
    ):
        innings.current_striker_id, innings.current_non_striker_id = (
            innings.current_non_striker_id,
            innings.current_striker_id,
        )

        db.commit()
        db.refresh(innings)