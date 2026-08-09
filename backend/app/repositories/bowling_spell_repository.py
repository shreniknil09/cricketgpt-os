from sqlalchemy.orm import Session

from app.models.bowler_match_stats import (
    BowlerMatchStats,
)


def get_player_bowling_stats(
    db: Session,
    player_id: int,
):
    return (
        db.query(BowlerMatchStats)
        .filter(
            BowlerMatchStats.player_id == player_id,
        )
        .order_by(
            BowlerMatchStats.match_id.desc(),
        )
        .all()
    )