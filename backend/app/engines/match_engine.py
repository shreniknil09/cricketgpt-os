from sqlalchemy.orm import Session

from app.models.ball import Ball

from app.engines.score_engine import update_score
from app.engines.batting_engine import update_batting_stats
from app.engines.bowling_engine import update_bowler_stats
from app.engines.strike_engine import rotate_strike
from app.engines.extras_engine import process_extras
from app.engines.over_engine import process_over
from app.engines.wicket_engine import process_wicket
from app.engines.innings_engine import process_innings


def process_ball(
    db: Session,
    ball: Ball,
):
    """
    Central Match Engine.

    Every ball delivered in the match passes through this engine.
    Each engine is responsible for handling one specific aspect
    of the game.
    """

    # ---------------------------------
    # Update Team Score
    # ---------------------------------
    update_score(
        db,
        ball,
    )

    # ---------------------------------
    # Update Batter Statistics
    # ---------------------------------
    update_batting_stats(
        db,
        ball,
    )

    # ---------------------------------
    # Update Bowler Statistics
    # ---------------------------------
    update_bowler_stats(
        db,
        ball,
    )

    # ---------------------------------
    # Rotate Strike
    # ---------------------------------
    rotate_strike(
        db,
        ball,
    )

    # ---------------------------------
    # Process Extras
    # ---------------------------------
    process_extras(
        db,
        ball,
    )

    # ---------------------------------
    # Process Over Completion
    # ---------------------------------
    process_over(
        db,
        ball,
    )

    # ---------------------------------
    # Process Wicket
    # ---------------------------------
    process_wicket(
        db,
        ball,
    )

    # ---------------------------------
    # Process Innings Completion
    # ---------------------------------
    process_innings(
        db,
        ball,
    )

    # ---------------------------------
    # Coming Next
    # ---------------------------------
    # process_result(db, ball)