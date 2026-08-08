from sqlalchemy.orm import Session

from app.models.player_match_stats import PlayerMatchStats
from app.models.bowler_match_stats import BowlerMatchStats


RECENT_MATCH_LIMIT = 5


def get_recent_batting_stats(
    db: Session,
    player_id: int,
):
    """
    Get the player's recent batting performances.
    """

    return (
        db.query(PlayerMatchStats)
        .filter(
            PlayerMatchStats.player_id == player_id,
        )
        .order_by(
            PlayerMatchStats.match_id.desc(),
        )
        .limit(RECENT_MATCH_LIMIT)
        .all()
    )


def get_recent_bowling_stats(
    db: Session,
    player_id: int,
):
    """
    Get the player's recent bowling performances.
    """

    return (
        db.query(BowlerMatchStats)
        .filter(
            BowlerMatchStats.player_id == player_id,
        )
        .order_by(
            BowlerMatchStats.match_id.desc(),
        )
        .limit(RECENT_MATCH_LIMIT)
        .all()
    )