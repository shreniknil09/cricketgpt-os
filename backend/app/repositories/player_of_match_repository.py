from sqlalchemy.orm import Session

from app.models.player_match_stats import PlayerMatchStats
from app.models.bowler_match_stats import BowlerMatchStats


def get_player_of_match_batting(
    db: Session,
    match_id: int,
):
    """
    Get batting statistics for a match.
    """

    return (
        db.query(PlayerMatchStats)
        .filter(
            PlayerMatchStats.match_id == match_id,
        )
        .all()
    )


def get_player_of_match_bowling(
    db: Session,
    match_id: int,
):
    """
    Get bowling statistics for a match.
    """

    return (
        db.query(BowlerMatchStats)
        .filter(
            BowlerMatchStats.match_id == match_id,
        )
        .all()
    )