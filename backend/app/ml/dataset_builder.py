from pathlib import Path

import pandas as pd


from app.ml.config import (
    FEATURE_COLUMNS,
    TARGET_COLUMN,
    TRAINING_DATA_PATH,
    DATA_DIR,
    MINIMUM_TRAINING_ROWS,
)


def build_training_dataset(
    records: list[dict],
    output_path: Path = TRAINING_DATA_PATH,
):
    """
    Build a CSV training dataset from match records.

    Each record must contain:
    - ML feature columns
    - team1_win target
    """

    if not records:
        raise ValueError(
            "No training records supplied."
        )

    dataframe = pd.DataFrame(
        records
    )

    required_columns = (
        FEATURE_COLUMNS
        + [TARGET_COLUMN]
    )

    missing_columns = [
        column
        for column in required_columns
        if column not in dataframe.columns
    ]

    if missing_columns:
        raise ValueError(
            "Missing training columns: "
            + ", ".join(missing_columns)
        )

    dataframe = dataframe[
        required_columns
    ].copy()

    # Convert feature columns to numeric
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

    dataframe = dataframe.drop_duplicates()

    if len(dataframe) < MINIMUM_TRAINING_ROWS:
        raise ValueError(
            f"At least {MINIMUM_TRAINING_ROWS} "
            "valid training rows are required."
        )

    dataframe[TARGET_COLUMN] = (
        dataframe[TARGET_COLUMN]
        .astype(int)
    )

    unique_targets = (
        dataframe[TARGET_COLUMN]
        .unique()
    )

    if len(unique_targets) < 2:
        raise ValueError(
            "Training data must contain both "
            "winning classes: 0 and 1."
        )

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    dataframe.to_csv(
        output_path,
        index=False,
    )

    return dataframe


def load_training_dataset(
    input_path: Path = TRAINING_DATA_PATH,
):
    if not input_path.exists():
        raise FileNotFoundError(
            f"Training dataset not found: "
            f"{input_path}"
        )

    dataframe = pd.read_csv(
        input_path
    )

    return dataframe