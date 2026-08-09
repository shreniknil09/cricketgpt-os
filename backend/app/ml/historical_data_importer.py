from pathlib import Path

import pandas as pd

from app.ml.config import (
    FEATURE_COLUMNS,
    TARGET_COLUMN,
    TRAINING_DATA_PATH,
)


REQUIRED_COLUMNS = [
    "team1_strength",
    "team2_strength",
    "team1_form",
    "team2_form",
    "team1_player_form",
    "team2_player_form",
    "venue_advantage",
    "head_to_head_advantage",
    "momentum",
    "pressure_index",
    "run_rate",
    "required_run_rate",
    "chase_difficulty",
    "match_impact",
    "team1_win",
]


def load_historical_csv(
    csv_path: str | Path,
):
    path = Path(csv_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Historical dataset not found: {path}"
        )

    dataframe = pd.read_csv(path)

    return dataframe


def validate_historical_dataset(
    dataframe: pd.DataFrame,
):
    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in dataframe.columns
    ]

    if missing_columns:
        raise ValueError(
            "Missing required columns: "
            + ", ".join(missing_columns)
        )

    dataframe = dataframe.copy()

    for column in FEATURE_COLUMNS:
        dataframe[column] = pd.to_numeric(
            dataframe[column],
            errors="coerce",
        )

    dataframe[TARGET_COLUMN] = pd.to_numeric(
        dataframe[TARGET_COLUMN],
        errors="coerce",
    )

    dataframe = dataframe.dropna()

    dataframe[TARGET_COLUMN] = (
        dataframe[TARGET_COLUMN]
        .astype(int)
    )

    invalid_targets = dataframe[
        ~dataframe[TARGET_COLUMN].isin([0, 1])
    ]

    if not invalid_targets.empty:
        raise ValueError(
            "team1_win must contain only 0 or 1."
        )

    if len(dataframe) < 20:
        raise ValueError(
            "At least 20 valid historical "
            "matches are required."
        )

    if dataframe[TARGET_COLUMN].nunique() < 2:
        raise ValueError(
            "Dataset must contain both "
            "winning classes: 0 and 1."
        )

    return dataframe


def import_historical_dataset(
    csv_path: str | Path,
):
    dataframe = load_historical_csv(
        csv_path
    )

    dataframe = validate_historical_dataset(
        dataframe
    )

    TRAINING_DATA_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    dataframe.to_csv(
        TRAINING_DATA_PATH,
        index=False,
    )

    return dataframe


if __name__ == "__main__":

    print(
        "Historical dataset importer."
    )

    print(
        "Usage:"
    )

    print(
        "from app.ml.historical_data_importer "
        "import import_historical_dataset"
    )