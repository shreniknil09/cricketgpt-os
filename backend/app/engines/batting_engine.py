from sqlalchemy.orm import Session

from app.models.ball import Ball
from app.models.over import Over
from app.models.innings import Innings
from app.models.player_match_stats import PlayerMatchStats


def update_batting_stats(
    db: Session,
    ball: Ball,
):
    """
    Updates batter statistics after every ball.
    """

    # Find the over
    over = (
        db.query(Over)
        .filter(Over.id == ball.over_id)
        .first()
    )

    if over is None:
        return

    # Find the innings
    innings = (
        db.query(Innings)
        .filter(Innings.id == over.innings_id)
        .first()
    )

    if innings is None:
        return

    # Find player's match stats
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

    # Update runs
    stats.runs += ball.runs

    # Wide does not count as a ball faced
    if ball.extra_type != "Wide":
        stats.balls += 1

    # Update boundaries
    if ball.runs == 4:
        stats.fours += 1

    if ball.runs == 6:
        stats.sixes += 1

    # Update strike rate
    if stats.balls > 0:
        stats.strike_rate = round(
            (stats.runs * 100) / stats.balls,
            2,
        )

    db.commit()