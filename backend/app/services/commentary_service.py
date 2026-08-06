from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.commentary_repository import (
    get_match_commentary,
)


def get_commentary(
    db: Session,
    match_id: int,
):
    commentary = get_match_commentary(
        db,
        match_id,
    )

    if len(commentary) == 0:
        raise HTTPException(
            status_code=404,
            detail="No commentary found.",
        )

    result = []

    for ball, over in commentary:

        result.append(
            {
                "over_number": over.over_number,
                "ball_number": ball.ball_number,
                "commentary": ball.commentary,
                "runs": ball.runs,
                "extra_type": ball.extra_type,
                "extra_runs": ball.extra_runs,
                "is_wicket": ball.is_wicket,
                "dismissal_type": ball.dismissal_type,
            }
        )

    return result