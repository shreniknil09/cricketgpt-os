import json
from pathlib import Path


RAW_DATA_DIR = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "ml"
    / "raw"
)


def load_match(file_path: Path) -> dict:
    with file_path.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def calculate_innings_features(innings: dict) -> dict:
    """
    Calculate basic batting features from one innings.
    """

    total_runs = 0
    total_balls = 0
    boundaries = 0
    dot_balls = 0
    wickets = 0

    overs = innings.get(
        "overs",
        []
    )

    for over in overs:

        deliveries = over.get(
            "deliveries",
            []
        )

        for delivery in deliveries:

            runs = delivery.get(
                "runs",
                {}
            )

            batter_runs = runs.get(
                "batter",
                0
            )

            extras = runs.get(
                "extras",
                0
            )

            total_runs += (
                batter_runs + extras
            )

            total_balls += 1

            if batter_runs in (4, 6):
                boundaries += 1

            if (
                batter_runs == 0
                and extras == 0
            ):
                dot_balls += 1

            if delivery.get(
                "wickets"
            ):
                wickets += len(
                    delivery["wickets"]
                )

    run_rate = (
        total_runs
        / (total_balls / 6)
        if total_balls
        else 0
    )

    boundary_rate = (
        boundaries
        / total_balls
        if total_balls
        else 0
    )

    dot_ball_rate = (
        dot_balls
        / total_balls
        if total_balls
        else 0
    )

    return {
        "runs": total_runs,
        "balls": total_balls,
        "wickets": wickets,
        "boundaries": boundaries,
        "dot_balls": dot_balls,
        "run_rate": round(
            run_rate,
            4,
        ),
        "boundary_rate": round(
            boundary_rate,
            4,
        ),
        "dot_ball_rate": round(
            dot_ball_rate,
            4,
        ),
    }


def calculate_match_features(
    data: dict,
) -> dict:

    innings_list = data.get(
        "innings",
        []
    )

    innings_features = []

    for innings in innings_list:

        features = (
            calculate_innings_features(
                innings
            )
        )

        features["team"] = (
            innings.get("team")
        )

        innings_features.append(
            features
        )

    total_runs = sum(
        item["runs"]
        for item in innings_features
    )

    total_wickets = sum(
        item["wickets"]
        for item in innings_features
    )

    total_balls = sum(
        item["balls"]
        for item in innings_features
    )

    total_boundaries = sum(
        item["boundaries"]
        for item in innings_features
    )

    total_dot_balls = sum(
        item["dot_balls"]
        for item in innings_features
    )

    overall_run_rate = (
        total_runs
        / (total_balls / 6)
        if total_balls
        else 0
    )

    return {
        "innings": innings_features,

        "total_runs": total_runs,

        "total_wickets": total_wickets,

        "total_balls": total_balls,

        "total_boundaries":
            total_boundaries,

        "total_dot_balls":
            total_dot_balls,

        "overall_run_rate":
            round(
                overall_run_rate,
                4,
            ),
    }


def extract_all_match_features(
    raw_directory: Path = RAW_DATA_DIR,
):

    json_files = sorted(
        raw_directory.glob("*.json")
    )

    if not json_files:
        raise FileNotFoundError(
            "No Cricsheet JSON files found."
        )

    results = []

    for file_path in json_files:

        try:

            data = load_match(
                file_path
            )

            match_features = (
                calculate_match_features(
                    data
                )
            )

            info = data.get(
                "info",
                {}
            )

            outcome = info.get(
                "outcome",
                {}
            )

            teams = info.get(
                "teams",
                []
            )

            match_features.update(
                {
                    "match_id":
                        file_path.stem,

                    "team1":
                        teams[0]
                        if len(teams) > 0
                        else None,

                    "team2":
                        teams[1]
                        if len(teams) > 1
                        else None,

                    "winner":
                        outcome.get(
                            "winner"
                        ),
                }
            )

            results.append(
                match_features
            )

        except Exception as error:

            print(
                f"Skipping "
                f"{file_path.name}: "
                f"{error}"
            )

    return results


if __name__ == "__main__":

    results = (
        extract_all_match_features()
    )

    print(
        f"Processed "
        f"{len(results)} matches."
    )

    if results:

        first = results[0]

        print(
            "\nFirst match:"
        )

        print(
            f"Teams: "
            f"{first['team1']} vs "
            f"{first['team2']}"
        )

        print(
            f"Winner: "
            f"{first['winner']}"
        )

        print(
            f"Total runs: "
            f"{first['total_runs']}"
        )

        print(
            f"Total balls: "
            f"{first['total_balls']}"
        )

        print(
            f"Boundaries: "
            f"{first['total_boundaries']}"
        )

        print(
            f"Dot balls: "
            f"{first['total_dot_balls']}"
        )

        print(
            f"Run rate: "
            f"{first['overall_run_rate']}"
        )