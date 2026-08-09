from typing import Any


from app.ml.config import FEATURE_COLUMNS


def _to_float(
    value: Any,
    default: float = 0.0,
) -> float:

    if value is None:
        return default

    try:
        return float(value)

    except (
        TypeError,
        ValueError,
    ):
        return default


def build_match_features(
    data: dict,
) -> dict:
    """
    Convert match analytics into a standardized
    ML feature dictionary.

    Missing values are safely converted to 0.0.
    """

    features = {
        "team1_strength": _to_float(
            data.get("team1_strength")
        ),

        "team2_strength": _to_float(
            data.get("team2_strength")
        ),

        "team1_form": _to_float(
            data.get("team1_form")
        ),

        "team2_form": _to_float(
            data.get("team2_form")
        ),

        "team1_player_form": _to_float(
            data.get("team1_player_form")
        ),

        "team2_player_form": _to_float(
            data.get("team2_player_form")
        ),

        "venue_advantage": _to_float(
            data.get("venue_advantage")
        ),

        "head_to_head_advantage": _to_float(
            data.get("head_to_head_advantage")
        ),

        "momentum": _to_float(
            data.get("momentum")
        ),

        "pressure_index": _to_float(
            data.get("pressure_index")
        ),

        "run_rate": _to_float(
            data.get("run_rate")
        ),

        "required_run_rate": _to_float(
            data.get("required_run_rate")
        ),

        "chase_difficulty": _to_float(
            data.get("chase_difficulty")
        ),

        "match_impact": _to_float(
            data.get("match_impact")
        ),
    }

    return {
        column: features.get(
            column,
            0.0,
        )
        for column in FEATURE_COLUMNS
    }


def build_feature_vector(
    data: dict,
) -> list[float]:
    """
    Return features in the exact order
    expected by the ML model.
    """

    features = build_match_features(
        data
    )

    return [
        features[column]
        for column in FEATURE_COLUMNS
    ]