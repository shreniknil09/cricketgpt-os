from sqlalchemy.orm import Session

from app.models.ball import Ball
from app.models.over import Over
from app.models.innings import Innings
from app.models.player_match_stats import PlayerMatchStats
from app.models.bowler_match_stats import BowlerMatchStats


def process_wicket(
    db: Session,
    ball: Ball,
):
    """
    Process wicket events.
    """

    # If no wicket, nothing to do
    if not ball.is_wicket:
        return

    # Find Over
    over = (
        db.query(Over)
        .filter(Over.id == ball.over_id)
        .first()
    )

    if over is None:
        return

    # Find Innings
    innings = (
        db.query(Innings)
        .filter(Innings.id == over.innings_id)
        .first()
    )

    if innings is None:
        return

    # Increase innings wickets
    innings.wickets += 1

    # Find batter stats
    batter_stats = (
        db.query(PlayerMatchStats)
        .filter(
            PlayerMatchStats.match_id == innings.match_id,
            PlayerMatchStats.player_id == ball.striker_id,
        )
        .first()
    )

    if batter_stats:
        batter_stats.is_out = True
        batter_stats.dismissal_type = ball.dismissal_type

    # Find bowler stats
    bowler_stats = (
        db.query(BowlerMatchStats)
        .filter(
            BowlerMatchStats.match_id == innings.match_id,
            BowlerMatchStats.player_id == ball.bowler_id,
        )
        .first()
    )

    if bowler_stats:
        bowler_stats.wickets += 1

    db.commit()
    db.refresh(innings)