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
    Check whether the current innings should end.
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
    # Find Current Innings
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
    # Start Innings
    # ---------------------------------

    if innings.status == "Not Started":
        innings.status = "In Progress"

    # ---------------------------------
    # Rule 1: All Wickets Lost
    # ---------------------------------

    if innings.wickets >= MAX_WICKETS:

        innings.status = "Completed"

    # ---------------------------------
    # Rule 2: Maximum Overs Completed
    # ---------------------------------

    elif innings.overs >= MAX_OVERS:

        innings.status = "Completed"

    # ---------------------------------
    # Rule 3: Chasing Team Reaches Target
    # ---------------------------------

    elif innings.innings_number == 2:

        first_innings = (
            db.query(Innings)
            .filter(
                Innings.match_id == innings.match_id,
                Innings.innings_number == 1,
            )
            .first()
        )

        if first_innings is not None:

            target = first_innings.runs + 1

            if innings.runs >= target:
                innings.status = "Completed"

    # ---------------------------------
    # Save Changes
    # ---------------------------------

    db.commit()
    db.refresh(innings)