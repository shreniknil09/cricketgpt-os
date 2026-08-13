from pathlib import Path

import pandas as pd

from app.ml.ball_by_ball_features import (
    extract_all_match_features,
)

from app.ml.v4_feature_engine import (
    build_v4_features,
)


# ============================================================
# Paths
# ============================================================

BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

OUTPUT_DIR = (
    BASE_DIR
    / "data"
    / "ml"
)

OUTPUT_PATH = (
    OUTPUT_DIR
    / "match_training_data_v4.csv"
)


# ============================================================
# Generate V4 Dataset
# ============================================================

def generate_v4_dataset():

    print(
        "Reading IPL historical data..."
    )

    matches = (
        extract_all_match_features()
    )

    print(
        f"Matches parsed: {len(matches)}"
    )

    if not matches:
        raise ValueError(
            "No historical matches were parsed."
        )

    print(
        "Building V4 chronological features..."
    )

    records = build_v4_features(
        matches
    )

    print(
        f"Valid training records: {len(records)}"
    )

    if not records:
        raise ValueError(
            "No valid V4 training records were generated."
        )

    dataframe = pd.DataFrame(
        records
    )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    dataframe.to_csv(
        OUTPUT_PATH,
        index=False,
    )

    print()
    print(
        "V4 dataset created successfully."
    )

    print()
    print(
        "Dataset path:"
    )

    print(
        OUTPUT_PATH
    )

    print()
    print(
        f"Dataset shape: {dataframe.shape}"
    )

    print()
    print(
        "Target distribution:"
    )

    print(
        dataframe[
            "team1_win"
        ].value_counts()
    )

    print()
    print(
        "Columns:"
    )

    print(
        list(
            dataframe.columns
        )
    )


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":
    generate_v4_dataset()