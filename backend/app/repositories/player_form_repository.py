from sqlalchemy.orm import Session

from app.models.player_match_stats import PlayerMatchStats
from app.models.bowler_match_stats import BowlerMatchStats


def get_batting_form(
    db: Session,
    player_id: int,
):
    """
    Get batting performances for a player.
    """

    return (
        db.query(PlayerMatchStats)
        .filter(
            PlayerMatchStats.player_id == player_id,
        )
        .order_by(
            PlayerMatchStats.match_id.desc(),
        )
        .limit(5)
        .all()
    )


def get_bowling_form(
    db: Session,
    player_id: int,
):
    """
    Get bowling performances for a player.
    """

    return (
        db.query(BowlerMatchStats)
        .filter(
            BowlerMatchStats.player_id == player_id,
        )
        .order_by(
            BowlerMatchStats.match_id.desc(),
        )
        .limit(5)
        .all()
    )