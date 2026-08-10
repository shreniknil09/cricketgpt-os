import pandas as pd
from pathlib import Path

from app.ml.cricsheet_parser import parse_all_matches
from app.ml.team_performance_engine import (
    build_team_performance_history,
)


OUTPUT_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "ml"
    / "match_training_data.csv"
)


def generate_dataset():

    print(
        "Reading IPL historical data..."
    )

    matches = parse_all_matches()

    print(
        f"Historical matches parsed: "
        f"{len(matches)}"
    )

    if not matches:
        raise ValueError(
            "No valid historical matches found."
        )

    print(
        "Building chronological "
        "team performance features..."
    )

    records = (
        build_team_performance_history(
            matches
        )
    )

    if not records:
        raise ValueError(
            "No training records generated."
        )

    dataframe = pd.DataFrame(
        records
    )

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    dataframe.to_csv(
        OUTPUT_PATH,
        index=False,
    )

    print(
        "\nTraining dataset created:"
    )

    print(
        OUTPUT_PATH
    )

    print(
        f"\nTraining rows: "
        f"{len(dataframe)}"
    )

    print(
        "\nTarget distribution:"
    )

    print(
        dataframe[
            "team1_win"
        ].value_counts()
    )

    print(
        "\nDataset shape:"
    )

    print(
        dataframe.shape
    )

    print(
        "\nColumns:"
    )

    print(
        list(
            dataframe.columns
        )
    )


if __name__ == "__main__":

    generate_dataset()