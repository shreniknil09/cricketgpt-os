import json
from pathlib import Path


RAW_DATA_DIR = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "ml"
    / "raw"
)


def load_match_json(file_path: Path) -> dict:
    with file_path.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def parse_match(file_path: Path) -> dict:
    data = load_match_json(file_path)

    info = data.get("info", {})

    teams = info.get("teams", [])
    dates = info.get("dates", [])
    outcome = info.get("outcome", {})
    toss = info.get("toss", {})

    return {
        "match_id": file_path.stem,

        "team1": (
            teams[0]
            if len(teams) > 0
            else None
        ),

        "team2": (
            teams[1]
            if len(teams) > 1
            else None
        ),

        "date": (
            str(dates[0])
            if dates
            else None
        ),

        "venue": info.get("venue"),

        "city": info.get("city"),

        "toss_winner": toss.get(
            "winner"
        ),

        "toss_decision": toss.get(
            "decision"
        ),

        "winner": outcome.get(
            "winner"
        ),

        "innings": data.get(
            "innings",
            [],
        ),
    }


def parse_all_matches(
    raw_directory: Path = RAW_DATA_DIR,
) -> list[dict]:

    if not raw_directory.exists():
        raise FileNotFoundError(
            f"Raw data directory not found: "
            f"{raw_directory}"
        )

    json_files = sorted(
        raw_directory.glob("*.json")
    )

    if not json_files:
        raise FileNotFoundError(
            "No JSON match files found in "
            f"{raw_directory}"
        )

    matches = []

    for file_path in json_files:

        try:
            match = parse_match(
                file_path
            )

            matches.append(match)

        except Exception as error:

            print(
                f"Skipping {file_path.name}: "
                f"{error}"
            )

    return matches


if __name__ == "__main__":

    matches = parse_all_matches()

    print(
        f"Successfully parsed "
        f"{len(matches)} matches."
    )

    if matches:

        first = matches[0]

        print("\nFirst match")
        print(
            f"ID: {first['match_id']}"
        )
        print(
            f"Teams: {first['team1']} "
            f"vs {first['team2']}"
        )
        print(
            f"Date: {first['date']}"
        )
        print(
            f"Venue: {first['venue']}"
        )
        print(
            f"Winner: {first['winner']}"
        )
        print(
            f"Innings: "
            f"{len(first['innings'])}"
        )