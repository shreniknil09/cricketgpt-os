from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.player_match_stats import PlayerMatchStats
from app.models.bowler_match_stats import BowlerMatchStats


def get_orange_cap(
    db: Session,
):
    """
    Player with the highest total runs.
    """

    return (
        db.query(
            PlayerMatchStats.player_id,
            func.sum(PlayerMatchStats.runs).label("total_runs"),
        )
        .group_by(PlayerMatchStats.player_id)
        .order_by(func.sum(PlayerMatchStats.runs).desc())
        .first()
    )


def get_purple_cap(
    db: Session,
):
    """
    Player with the highest total wickets.
    """

    return (
        db.query(
            BowlerMatchStats.player_id,
            func.sum(BowlerMatchStats.wickets).label("total_wickets"),
        )
        .group_by(BowlerMatchStats.player_id)
        .order_by(func.sum(BowlerMatchStats.wickets).desc())
        .first()
    )


def get_most_sixes(
    db: Session,
):
    """
    Player with the most sixes.
    """

    return (
        db.query(
            PlayerMatchStats.player_id,
            func.sum(PlayerMatchStats.sixes).label("total_sixes"),
        )
        .group_by(PlayerMatchStats.player_id)
        .order_by(func.sum(PlayerMatchStats.sixes).desc())
        .first()
    )


def get_most_fours(
    db: Session,
):
    """
    Player with the most fours.
    """

    return (
        db.query(
            PlayerMatchStats.player_id,
            func.sum(PlayerMatchStats.fours).label("total_fours"),
        )
        .group_by(PlayerMatchStats.player_id)
        .order_by(func.sum(PlayerMatchStats.fours).desc())
        .first()
    )