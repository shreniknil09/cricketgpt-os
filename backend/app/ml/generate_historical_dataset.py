from pathlib import Path

import pandas as pd

from app.ml.ball_by_ball_features import (
    extract_all_match_features,
)


OUTPUT_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "ml"
    / "match_training_data.csv"
)


def calculate_team_features(
    match: dict,
):
    """
    Convert parsed historical match data
    into a basic supervised-learning record.

    These are real historical features extracted
    from Cricsheet data.
    """

    innings = match.get(
        "innings",
        []
    )

    team1 = match.get(
        "team1"
    )

    team2 = match.get(
        "team2"
    )

    winner = match.get(
        "winner"
    )

    team1_innings = [
        item
        for item in innings
        if item.get("team") == team1
    ]

    team2_innings = [
        item
        for item in innings
        if item.get("team") == team2
    ]

    team1_runs = sum(
        item.get("runs", 0)
        for item in team1_innings
    )

    team2_runs = sum(
        item.get("runs", 0)
        for item in team2_innings
    )

    team1_balls = sum(
        item.get("balls", 0)
        for item in team1_innings
    )

    team2_balls = sum(
        item.get("balls", 0)
        for item in team2_innings
    )

    team1_boundaries = sum(
        item.get("boundaries", 0)
        for item in team1_innings
    )

    team2_boundaries = sum(
        item.get("boundaries", 0)
        for item in team2_innings
    )

    team1_dots = sum(
        item.get("dot_balls", 0)
        for item in team1_innings
    )

    team2_dots = sum(
        item.get("dot_balls", 0)
        for item in team2_innings
    )

    team1_run_rate = (
        team1_runs
        / (team1_balls / 6)
        if team1_balls
        else 0
    )

    team2_run_rate = (
        team2_runs
        / (team2_balls / 6)
        if team2_balls
        else 0
    )

    team1_boundary_rate = (
        team1_boundaries
        / team1_balls
        if team1_balls
        else 0
    )

    team2_boundary_rate = (
        team2_boundaries
        / team2_balls
        if team2_balls
        else 0
    )

    team1_dot_rate = (
        team1_dots
        / team1_balls
        if team1_balls
        else 0
    )

    team2_dot_rate = (
        team2_dots
        / team2_balls
        if team2_balls
        else 0
    )

    if winner == team1:
        team1_win = 1

    elif winner == team2:
        team1_win = 0

    else:
        return None

    return {
        "match_id": match.get(
            "match_id"
        ),

        "team1": team1,

        "team2": team2,

        # Team 1 historical performance
        "team1_strength": round(
            team1_run_rate
            + (
                team1_boundary_rate
                * 10
            )
            + (
                team1_dot_rate
                * 5
            ),
            4,
        ),

        # Team 2 historical performance
        "team2_strength": round(
            team2_run_rate
            + (
                team2_boundary_rate
                * 10
            )
            + (
                team2_dot_rate
                * 5
            ),
            4,
        ),

        "team1_form": round(
            team1_run_rate,
            4,
        ),

        "team2_form": round(
            team2_run_rate,
            4,
        ),

        "team1_player_form": 0.0,

        "team2_player_form": 0.0,

        "venue_advantage": 0.0,

        "head_to_head_advantage": round(
            team1_run_rate
            - team2_run_rate,
            4,
        ),

        "momentum": round(
            team1_run_rate
            - team2_run_rate,
            4,
        ),

        "pressure_index": round(
            abs(
                team1_run_rate
                - team2_run_rate
            ),
            4,
        ),

        "run_rate": round(
            (
                team1_run_rate
                + team2_run_rate
            ) / 2,
            4,
        ),

        "required_run_rate": 0.0,

        "chase_difficulty": 0.0,

        "match_impact": round(
            (
                team1_run_rate
                - team2_run_rate
            ),
            4,
        ),

        "team1_win": team1_win,
    }


def generate_dataset():

    print(
        "Reading IPL historical data..."
    )

    matches = (
        extract_all_match_features()
    )

    print(
        f"Matches parsed: {len(matches)}"
    )

    records = []

    for match in matches:

        record = calculate_team_features(
            match
        )

        if record is not None:
            records.append(
                record
            )

    if not records:
        raise ValueError(
            "No valid historical "
            "training records found."
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
        f"Training dataset created:"
    )

    print(
        OUTPUT_PATH
    )

    print(
        f"Training rows: "
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
        "\nColumns:"
    )

    print(
        list(
            dataframe.columns
        )
    )


if __name__ == "__main__":
    generate_dataset()