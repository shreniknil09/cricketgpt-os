from sqlalchemy.orm import Session

from app.models.ball import Ball
from app.models.over import Over
from app.models.innings import Innings


MAX_OVERS = 20
MAX_WICKETS = 10


def process_innings(
    db: Session,
    ball: Ball,
):
    """
    Check whether the innings should end.
    """

    # Find the over
    over = (
        db.query(Over)
        .filter(Over.id == ball.over_id)
        .first()
    )

    if over is None:
        return

    # Find innings
    innings = (
        db.query(Innings)
        .filter(Innings.id == over.innings_id)
        .first()
    )

    if innings is None:
        return

    # End innings if wickets reached
    if innings.wickets >= MAX_WICKETS:
        innings.status = "Completed"

    # End innings if overs completed
    elif innings.overs >= MAX_OVERS:
        innings.status = "Completed"

    db.commit()
    db.refresh(innings)