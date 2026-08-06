from sqlalchemy.orm import Session

from app.models.ball import Ball
from app.models.over import Over
from app.models.innings import Innings


def update_score(
    db: Session,
    ball: Ball,
):
    """
    Updates Over and Innings after every ball.
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

    # -------------------------
    # Update Runs
    # -------------------------

    total_runs = ball.runs + ball.extra_runs

    over.runs += total_runs
    innings.runs += total_runs

    # -------------------------
    # Update Wickets
    # -------------------------

    if ball.is_wicket:
        over.wickets += 1
        innings.wickets += 1

    # -------------------------
    # Update Balls
    # Wide and No Ball
    # are NOT legal deliveries
    # -------------------------

    if ball.extra_type not in ["Wide", "No Ball"]:

        innings.balls += 1

        if innings.balls == 6:
            innings.overs += 1
            innings.balls = 0

            over.status = "Completed"

    # -------------------------
    # Complete Innings
    # -------------------------

    if (
        innings.overs >= 20
        or innings.wickets >= 10
    ):
        innings.status = "Completed"

    db.commit()