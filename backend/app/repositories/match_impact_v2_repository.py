from sqlalchemy.orm import Session

from app.models.match import Match
from app.models.player_match_stats import (
    PlayerMatchStats,
)


def get_match(
    db: Session,
    match_id: int,
):
    return (
        db.query(Match)
        .filter(
            Match.id == match_id,
        )
        .first()
    )


def get_match_player_stats(
    db: Session,
    match_id: int,
):
    return (
        db.query(PlayerMatchStats)
        .filter(
            PlayerMatchStats.match_id == match_id,
        )
        .all()
    )