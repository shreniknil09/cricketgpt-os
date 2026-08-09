from app.ml.feature_engineering import (
    build_match_features,
)

from app.ml.model_loader import (
    load_model,
)


def predict_match(
    data: dict,
):
    """
    Generate match prediction using
    the trained ML model.
    """

    model = load_model()

    features = build_match_features(
        data
    )

    prediction_input = [
        [
            features[column]
            for column in features
        ]
    ]

    prediction = model.predict(
        prediction_input
    )[0]

    probabilities = (
        model.predict_proba(
            prediction_input
        )[0]
    )

    team1_probability = (
        float(probabilities[1])
        * 100
    )

    team2_probability = (
        float(probabilities[0])
        * 100
    )

    predicted_winner = (
        1
        if prediction == 1
        else 2
    )

    confidence = max(
        team1_probability,
        team2_probability,
    )

    return {
        "predicted_winner":
            predicted_winner,

        "team1_win_probability":
            round(
                team1_probability,
                2,
            ),

        "team2_win_probability":
            round(
                team2_probability,
                2,
            ),

        "confidence":
            round(
                confidence,
                2,
            ),
    }