from sqlalchemy.orm import Session

from app.models.ball import Ball

from app.services.score_engine import update_score
from app.services.player_stats_engine import update_player_stats
from app.services.bowler_stats_engine import update_bowler_stats


def process_ball(
    db: Session,
    ball: Ball,
):
    """
    Central Cricket Match Engine
    """

    # Update Score
    update_score(
        db,
        ball,
    )

    # Update Batter Statistics
    update_player_stats(
        db,
        ball,
    )

    # Update Bowler Statistics
    update_bowler_stats(
        db,
        ball,
    )

    # Upcoming Engines
    # rotate_strike(db, ball)
    # handle_extras(db, ball)
    # handle_wicket(db, ball)
    # complete_over(db, ball)
    # complete_match(db, ball)