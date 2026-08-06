from sqlalchemy.orm import Session

from app.models.innings import Innings


def get_live_score(
    db: Session,
    match_id: int,
):
    """
    Returns the current active innings
    for a given match.
    """

    return (
        db.query(Innings)
        .filter(
            Innings.match_id == match_id,
            Innings.status != "Completed",
        )
        .order_by(Innings.innings_number.desc())
        .first()
    )