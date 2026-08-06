from sqlalchemy.orm import Session

from app.models.ball import Ball
from app.models.over import Over
from app.models.innings import Innings
from app.models.bowler_match_stats import BowlerMatchStats


def update_bowler_stats(
    db: Session,
    ball: Ball,
):
    """
    Updates bowling statistics after every ball.
    """

    # Get the over
    over = (
        db.query(Over)
        .filter(Over.id == ball.over_id)
        .first()
    )

    if over is None:
        return

    # Get innings
    innings = (
        db.query(Innings)
        .filter(Innings.id == over.innings_id)
        .first()
    )

    if innings is None:
        return

    # Get bowler stats
    stats = (
        db.query(BowlerMatchStats)
        .filter(
            BowlerMatchStats.match_id == innings.match_id,
            BowlerMatchStats.player_id == ball.bowler_id,
        )
        .first()
    )

    if stats is None:
        return

    # -------------------------
    # Runs conceded
    # -------------------------

    stats.runs_given += (
        ball.runs + ball.extra_runs
    )

    # -------------------------
    # Legal delivery
    # Wide and No Ball do NOT count
    # -------------------------

    if ball.extra_type not in ["Wide", "No Ball"]:

        stats.balls += 1

        stats.overs = (
            stats.balls // 6
        ) + (
            (stats.balls % 6) / 10
        )

    # -------------------------
    # Wicket
    # -------------------------

    if ball.is_wicket:
        stats.wickets += 1

    # -------------------------
    # Economy
    # -------------------------

    if stats.balls > 0:

        overs_float = stats.balls / 6

        stats.economy = (
            stats.runs_given / overs_float
        )

    db.commit()