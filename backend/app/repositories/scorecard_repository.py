from sqlalchemy.orm import Session

from app.models.innings import Innings
from app.models.player_match_stats import PlayerMatchStats
from app.models.bowler_match_stats import BowlerMatchStats


def get_innings_score(
    db: Session,
    match_id: int,
):
    return (
        db.query(Innings)
        .filter(Innings.match_id == match_id)
        .order_by(Innings.innings_number.desc())
        .first()
    )


def get_batting_scorecard(
    db: Session,
    match_id: int,
):
    return (
        db.query(PlayerMatchStats)
        .filter(
            PlayerMatchStats.match_id == match_id
        )
        .all()
    )


def get_bowling_scorecard(
    db: Session,
    match_id: int,
):
    return (
        db.query(BowlerMatchStats)
        .filter(
            BowlerMatchStats.match_id == match_id
        )
        .all()
    )