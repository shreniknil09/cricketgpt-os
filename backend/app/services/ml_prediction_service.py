from fastapi import HTTPException
from sqlalchemy.orm import Session

from sklearn.linear_model import LogisticRegression

from app.repositories.ml_prediction_repository import (
    get_completed_matches,
    get_match,
)


MINIMUM_TRAINING_MATCHES = 10


def _build_features(
    match,
):
    """
    Build numerical features for a match.

    Features:
    1. Team 1 ID
    2. Team 2 ID
    3. Toss winner
    """

    toss_team1 = 0

    if match.toss_winner_id == match.team1_id:
        toss_team1 = 1

    elif match.toss_winner_id == match.team2_id:
        toss_team1 = 0.0

    return [
        match.team1_id,
        match.team2_id,
        toss_team1,
    ]


def get_ml_prediction(
    db: Session,
    match_id: int,
):
    """
    Train a baseline Logistic Regression model
    using historical completed matches and predict
    the winner for the requested match.
    """

    # ---------------------------------
    # Get requested match
    # ---------------------------------

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
    # Get historical matches
    # ---------------------------------

    historical_matches = get_completed_matches(
        db,
    )

    # Don't train using the match we're
    # trying to predict if it is completed.

    historical_matches = [
        historical_match
        for historical_match in historical_matches
        if historical_match.id != match_id
    ]

    if len(historical_matches) < MINIMUM_TRAINING_MATCHES:
        raise HTTPException(
            status_code=400,
            detail=(
                "At least 10 completed historical "
                "matches are required to train the "
                "ML prediction model."
            ),
        )

    # ---------------------------------
    # Build training dataset
    # ---------------------------------

    X = []
    y = []

    for historical_match in historical_matches:

        features = _build_features(
            historical_match
        )

        X.append(features)

        # Binary target:
        # 1 = team1 won
        # 0 = team2 won

        if (
            historical_match.winner_id
            == historical_match.team1_id
        ):
            y.append(1)

        else:
            y.append(0)

    # ---------------------------------
    # Train Logistic Regression
    # ---------------------------------

    model = LogisticRegression(
        max_iter=1000,
    )

    model.fit(
        X,
        y,
    )

    # ---------------------------------
    # Predict requested match
    # ---------------------------------

    prediction_features = [
        _build_features(match)
    ]

    probabilities = model.predict_proba(
        prediction_features
    )[0]

    # Find which class represents
    # team 1 winning.

    class_probabilities = dict(
        zip(
            model.classes_,
            probabilities,
        )
    )

    team1_probability = (
        class_probabilities.get(
            1,
            0.0,
        )
        * 100
    )

    team2_probability = (
        class_probabilities.get(
            0,
            0.0,
        )
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
    # Return
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

        "model": "Logistic Regression",
    }