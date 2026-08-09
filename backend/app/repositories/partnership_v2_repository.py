from sqlalchemy.orm import Session

from app.models.innings import Innings
from app.models.over import Over
from app.models.ball import Ball


def get_innings(
    db: Session,
    match_id: int,
):
    return (
        db.query(Innings)
        .filter(
            Innings.match_id == match_id,
        )
        .order_by(
            Innings.id.desc(),
        )
        .first()
    )


def get_innings_balls(
    db: Session,
    innings_id: int,
):
    return (
        db.query(Ball)
        .join(
            Over,
            Ball.over_id == Over.id,
        )
        .filter(
            Over.innings_id == innings_id,
        )
        .order_by(
            Over.over_number.asc(),
            Ball.ball_number.asc(),
        )
        .all()
    )


def get_partnerships(
    db: Session,
    innings_id: int,
):
    """
    Build partnerships directly from ball-by-ball data.

    A partnership consists of runs scored while the same
    striker/non-striker combination is batting.
    """

    balls = get_innings_balls(
        db,
        innings_id,
    )

    partnerships = []

    if not balls:
        return partnerships

    current_striker = balls[0].striker_id
    current_non_striker = balls[0].non_striker_id

    partnership_runs = 0

    for ball in balls:

        # Detect a new batting pair
        if (
            ball.striker_id != current_striker
            or ball.non_striker_id != current_non_striker
        ):
            if partnership_runs > 0:
                partnerships.append(
                    {
                        "striker_id": current_striker,
                        "non_striker_id": current_non_striker,
                        "runs": partnership_runs,
                    }
                )

            current_striker = ball.striker_id
            current_non_striker = ball.non_striker_id
            partnership_runs = 0

        # Add runs from this delivery
        partnership_runs += (
            ball.runs or 0
        )

        # If wicket occurs, close this partnership
        if ball.is_wicket:

            if partnership_runs > 0:
                partnerships.append(
                    {
                        "striker_id": current_striker,
                        "non_striker_id": current_non_striker,
                        "runs": partnership_runs,
                    }
                )

            partnership_runs = 0

            # Next ball will establish the new pair

    # Save final partnership
    if partnership_runs > 0:
        partnerships.append(
            {
                "striker_id": current_striker,
                "non_striker_id": current_non_striker,
                "runs": partnership_runs,
            }
        )

    return partnerships