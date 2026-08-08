from sqlalchemy.orm import Session

from app.models.innings import Innings


def get_current_innings(
    db: Session,
    match_id: int,
):
    """
    Get the current innings of a match.

    For a live match, the second innings is treated
    as the active chasing innings.
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

    # Fallback to first innings if second innings
    # has not started yet.

    return (
        db.query(Innings)
        .filter(
            Innings.match_id == match_id,
            Innings.innings_number == 1,
        )
        .first()
    )


def get_first_innings(
    db: Session,
    match_id: int,
):
    """
    Get the first innings of a match.
    """

    return (
        db.query(Innings)
        .filter(
            Innings.match_id == match_id,
            Innings.innings_number == 1,
        )
        .first()
    )