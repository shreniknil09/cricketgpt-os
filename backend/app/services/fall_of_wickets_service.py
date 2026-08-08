from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.fall_of_wickets_repository import (
    get_innings_wickets,
)


def get_fall_of_wickets(
    db: Session,
    innings_id: int,
):
    """
    Generate fall-of-wickets information
    for an innings.
    """

    wicket_records = get_innings_wickets(
        db,
        innings_id,
    )

    if not wicket_records:
        raise HTTPException(
            status_code=404,
            detail="No wickets found for this innings.",
        )

    fall_of_wickets = []

    wicket_number = 1

    for ball, over in wicket_records:

        # ---------------------------------
        # Calculate Score at Wicket
        # ---------------------------------

        score = ball.runs

        # ---------------------------------
        # Get all balls before/current
        # ---------------------------------

        previous_balls = (
            db.query(ball.__class__)
            .join(
                over.__class__,
                ball.__class__.over_id == over.__class__.id,
            )
            .filter(
                over.__class__.innings_id == innings_id,
            )
            .all()
        )

        total_score = 0

        for previous_ball in previous_balls:

            if (
                previous_ball.id
                <= ball.id
            ):
                total_score += (
                    previous_ball.runs
                )

        # ---------------------------------
        # Over notation
        # ---------------------------------

        over_number = over.over_number
        ball_number = ball.ball_number

        over_value = float(
            f"{over_number}.{ball_number}"
        )

        # ---------------------------------
        # Dismissed Player
        # ---------------------------------

        player_id = ball.striker_id

        # ---------------------------------
        # Add Fall of Wicket
        # ---------------------------------

        fall_of_wickets.append(
            {
                "innings_id": innings_id,
                "wicket_number": wicket_number,
                "player_id": player_id,
                "score": total_score,
                "over": over_value,
            }
        )

        wicket_number += 1

    return fall_of_wickets