from sqlalchemy.orm import Session

from app.models.ball import Ball
from app.models.over import Over
from app.models.innings import Innings
from app.models.player_match_stats import PlayerMatchStats


def update_player_stats(
    db: Session,
    ball: Ball,
):
    """
    Updates batting statistics after every ball.
    """

    over = (
        db.query(Over)
        .filter(Over.id == ball.over_id)
        .first()
    )

    if over is None:
        return

    innings = (
        db.query(Innings)
        .filter(Innings.id == over.innings_id)
        .first()
    )

    if innings is None:
        return

    stats = (
        db.query(PlayerMatchStats)
        .filter(
            PlayerMatchStats.match_id == innings.match_id,
            PlayerMatchStats.player_id == ball.striker_id,
        )
        .first()
    )

    if stats is None:
        return

    # Runs
    stats.runs += ball.runs

    # Ball faced
    if ball.extra_type not in ["Wide"]:
        stats.balls += 1

    # Boundary
    if ball.runs == 4:
        stats.fours += 1

    if ball.runs == 6:
        stats.sixes += 1

    # Strike Rate

    if stats.balls > 0:
        stats.strike_rate = (
            stats.runs * 100
        ) / stats.balls

    db.commit()