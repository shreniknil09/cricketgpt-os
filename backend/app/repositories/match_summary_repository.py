from sqlalchemy.orm import Session

from app.models.match import Match
from app.models.innings import Innings


def get_match(
    db: Session,
    match_id: int,
):
    return (
        db.query(Match)
        .filter(Match.id == match_id)
        .first()
    )


def get_match_innings(
    db: Session,
    match_id: int,
):
    return (
        db.query(Innings)
        .filter(
            Innings.match_id == match_id
        )
        .order_by(Innings.innings_number)
        .all()
    )