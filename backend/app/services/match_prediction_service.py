from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.match_prediction_repository import (
    get_match,
)


def get_match_prediction(
    db: Session,
    match_id: int,
):
    """
    Generate a basic pre-match prediction.

    Version 1 uses a transparent rule-based model.
    """

    match = get_match(
        db,
        match_id,
    )

    if match is None:
        raise HTTPException(
            status_code=404,
            detail="Match not found.",
        )

    # ---------------------------------
    # Base Probability
    # ---------------------------------

    team1_probability = 50.0
    team2_probability = 50.0

    # ---------------------------------
    # Toss Advantage
    # ---------------------------------

    if match.toss_winner_id is not None:

        if match.toss_winner_id == match.team1_id:
            team1_probability += 5.0
            team2_probability -= 5.0

        elif match.toss_winner_id == match.team2_id:
            team2_probability += 5.0
            team1_probability -= 5.0

    # ---------------------------------
    # Normalize
    # ---------------------------------

    total = (
        team1_probability
        + team2_probability
    )

    team1_probability = (
        team1_probability
        / total
        * 100
    )

    team2_probability = (
        team2_probability
        / total
        * 100
    )

    # ---------------------------------
    # Predicted Winner
    # ---------------------------------

    if (
        team1_probability
        >= team2_probability
    ):
        predicted_winner_id = (
            match.team1_id
        )

    else:
        predicted_winner_id = (
            match.team2_id
        )

    # ---------------------------------
    # Return Prediction
    # ---------------------------------

    return {
        "match_id": match.id,

        "team1_id": match.team1_id,

        "team2_id": match.team2_id,

        "team1_probability": round(
            team1_probability,
            2,
        ),

        "team2_probability": round(
            team2_probability,
            2,
        ),

        "predicted_winner_id": (
            predicted_winner_id
        ),
    }