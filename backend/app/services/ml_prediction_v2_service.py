from fastapi import HTTPException
from sqlalchemy.orm import Session

from sklearn.linear_model import LogisticRegression

from app.repositories.ml_prediction_v2_repository import (
    get_match,
    get_completed_matches,
)

from app.services.team_strength_service import (
    get_team_strength,
)

from app.services.team_form_service import (
    get_team_form,
)

from app.services.venue_analysis_service import (
    get_venue_analysis,
)

from app.services.head_to_head_service import (
    get_head_to_head,
)


MINIMUM_TRAINING_MATCHES = 10


def _safe_team_strength(
    db: Session,
    team_id: int,
):
    """
    Get team strength safely.
    """

    try:

        result = get_team_strength(
            db,
            team_id,
        )

        return result["overall_strength"]

    except HTTPException:

        return 50.0


def _safe_team_form(
    db: Session,
    team_id: int,
):
    """
    Get team form safely.
    """

    try:

        result = get_team_form(
            db,
            team_id,
        )

        return result["form_rating"]

    except HTTPException:

        return 50.0


def _safe_venue_rating(
    db: Session,
    team_id: int,
    venue_id: int,
):
    """
    Get venue performance safely.
    """

    try:

        result = get_venue_analysis(
            db,
            team_id,
            venue_id,
        )

        return result["venue_rating"]

    except HTTPException:

        return 50.0


def _safe_head_to_head(
    db: Session,
    team1_id: int,
    team2_id: int,
):
    """
    Get head-to-head win rate safely.
    """

    try:

        result = get_head_to_head(
            db,
            team1_id,
            team2_id,
        )

        return (
            result["team1_win_rate"],
            result["team2_win_rate"],
        )

    except HTTPException:

        return 50.0, 50.0


def _build_features(
    db: Session,
    match,
):
    """
    Build advanced prediction features.

    Features:

    1. Team 1 strength
    2. Team 2 strength
    3. Team 1 form
    4. Team 2 form
    5. Team 1 venue rating
    6. Team 2 venue rating
    7. Team 1 H2H rate
    8. Team 2 H2H rate
    9. Toss advantage
    """

    team1_strength = _safe_team_strength(
        db,
        match.team1_id,
    )

    team2_strength = _safe_team_strength(
        db,
        match.team2_id,
    )

    team1_form = _safe_team_form(
        db,
        match.team1_id,
    )

    team2_form = _safe_team_form(
        db,
        match.team2_id,
    )

    team1_venue = _safe_venue_rating(
        db,
        match.team1_id,
        match.venue_id,
    )

    team2_venue = _safe_venue_rating(
        db,
        match.team2_id,
        match.venue_id,
    )

    team1_h2h, team2_h2h = (
        _safe_head_to_head(
            db,
            match.team1_id,
            match.team2_id,
        )
    )

    # 1 = Team 1 won toss
    # 0 = Team 2 won toss
    # 0.5 = toss not available

    if match.toss_winner_id == match.team1_id:

        toss_advantage = 1.0

    elif match.toss_winner_id == match.team2_id:

        toss_advantage = 0.0

    else:

        toss_advantage = 0.5

    return [
        team1_strength,
        team2_strength,
        team1_form,
        team2_form,
        team1_venue,
        team2_venue,
        team1_h2h,
        team2_h2h,
        toss_advantage,
    ]


def get_ml_prediction_v2(
    db: Session,
    match_id: int,
):
    """
    Train and execute the advanced ML prediction model.
    """

    # ---------------------------------
    # Requested Match
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
    # Historical Matches
    # ---------------------------------

    historical_matches = (
        get_completed_matches(db)
    )

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
                "matches are required for ML Prediction V2."
            ),
        )

    # ---------------------------------
    # Build Training Dataset
    # ---------------------------------

    X = []
    y = []

    for historical_match in historical_matches:

        features = _build_features(
            db,
            historical_match,
        )

        X.append(features)

        if (
            historical_match.winner_id
            == historical_match.team1_id
        ):

            y.append(1)

        else:

            y.append(0)

    # ---------------------------------
    # Train Model
    # ---------------------------------

    model = LogisticRegression(
        max_iter=2000,
    )

    model.fit(
        X,
        y,
    )

    # ---------------------------------
    # Prediction Features
    # ---------------------------------

    prediction_features = [
        _build_features(
            db,
            match,
        )
    ]

    probabilities = model.predict_proba(
        prediction_features
    )[0]

    probability_map = dict(
        zip(
            model.classes_,
            probabilities,
        )
    )

    team1_probability = (
        probability_map.get(
            1,
            0.5,
        )
        * 100
    )

    team2_probability = (
        probability_map.get(
            0,
            0.5,
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

        "model": "Logistic Regression - Advanced Features",
    }