from sqlalchemy.orm import Session

from app.models.player_match_stats import PlayerMatchStats
from app.models.bowler_match_stats import BowlerMatchStats


def get_batting_career(
    db: Session,
    player_id: int,
):
    """
    Get all batting records of a player.
    """

    return (
        db.query(PlayerMatchStats)
        .filter(
            PlayerMatchStats.player_id == player_id,
        )
        .all()
    )


def get_bowling_career(
    db: Session,
    player_id: int,
):
    """
    Get all bowling records of a player.
    """

    return (
        db.query(BowlerMatchStats)
        .filter(
            BowlerMatchStats.player_id == player_id,
        )
        .all()
    )