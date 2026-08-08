from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.partnership_repository import (
    get_innings_balls,
)


def get_partnerships(
    db: Session,
    innings_id: int,
):
    """
    Calculate batting partnerships for an innings.
    """

    balls = get_innings_balls(
        db,
        innings_id,
    )

    if not balls:
        raise HTTPException(
            status_code=404,
            detail="No balls found for this innings.",
        )

    partnerships = {}

    for ball in balls:

        striker_id = ball.striker_id
        non_striker_id = ball.non_striker_id

        # ---------------------------------
        # Ignore incomplete ball records
        # ---------------------------------

        if (
            striker_id is None
            or non_striker_id is None
        ):
            continue

        # ---------------------------------
        # Create consistent pair
        # ---------------------------------

        pair = tuple(
            sorted(
                [
                    striker_id,
                    non_striker_id,
                ]
            )
        )

        # ---------------------------------
        # Create partnership
        # ---------------------------------

        if pair not in partnerships:

            partnerships[pair] = {
                "innings_id": innings_id,
                "striker_id": pair[0],
                "non_striker_id": pair[1],
                "runs": 0,
                "balls": 0,
            }

        # ---------------------------------
        # Add runs
        # ---------------------------------

        partnerships[pair]["runs"] += (
            ball.runs
        )

        # ---------------------------------
        # Count legal deliveries
        # ---------------------------------

        if ball.extra_type not in [
            "Wide",
            "No Ball",
        ]:
            partnerships[pair]["balls"] += 1

    # ---------------------------------
    # Return partnerships
    # ---------------------------------

    return list(
        partnerships.values()
    )