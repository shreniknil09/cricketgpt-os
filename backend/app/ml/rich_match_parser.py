import json
from pathlib import Path


# ============================================================
# Paths
# ============================================================

RAW_DATA_DIR = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "ml"
    / "raw"
)


# ============================================================
# JSON Loader
# ============================================================

def load_match(file_path: Path) -> dict:
    """
    Load one Cricsheet JSON match file.
    """

    with file_path.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


# ============================================================
# Delivery Parser
# ============================================================

def parse_delivery(
    delivery: dict,
) -> dict:
    """
    Extract useful information from one delivery.
    """

    runs = delivery.get(
        "runs",
        {},
    )

    batter_runs = runs.get(
        "batter",
        0,
    )

    extras_runs = runs.get(
        "extras",
        0,
    )

    total_runs = runs.get(
        "total",
        batter_runs + extras_runs,
    )

    wickets = []

    for wicket in delivery.get(
        "wickets",
        [],
    ):

        wickets.append(
            {
                "player_out":
                    wicket.get(
                        "player_out"
                    ),

                "kind":
                    wicket.get(
                        "kind"
                    ),

                "fielders":
                    wicket.get(
                        "fielders",
                        [],
                    ),
            }
        )

    return {
        "batter":
            delivery.get(
                "batter"
            ),

        "bowler":
            delivery.get(
                "bowler"
            ),

        "non_striker":
            delivery.get(
                "non_striker"
            ),

        "batter_runs":
            batter_runs,

        "extras_runs":
            extras_runs,

        "total_runs":
            total_runs,

        "extras":
            delivery.get(
                "extras",
                {},
            ),

        "wickets":
            wickets,
    }


# ============================================================
# Innings Parser
# ============================================================

def parse_innings(
    innings: dict,
    innings_number: int,
) -> dict:
    """
    Parse one complete innings while retaining
    over and delivery information.
    """

    team = innings.get(
        "team"
    )

    overs = []

    total_runs = 0
    total_wickets = 0
    total_balls = 0
    total_boundaries = 0
    total_dot_balls = 0

    for over in innings.get(
        "overs",
        [],
    ):

        over_number = over.get(
            "over"
        )

        deliveries = []

        over_runs = 0
        over_balls = 0
        over_wickets = 0

        for delivery in over.get(
            "deliveries",
            [],
        ):

            parsed = parse_delivery(
                delivery
            )

            deliveries.append(
                parsed
            )

            total_runs += (
                parsed[
                    "total_runs"
                ]
            )

            over_runs += (
                parsed[
                    "total_runs"
                ]
            )

            total_balls += 1
            over_balls += 1

            batter_runs = parsed[
                "batter_runs"
            ]

            if batter_runs in (
                4,
                6,
            ):
                total_boundaries += 1

            if (
                batter_runs == 0
                and parsed[
                    "extras_runs"
                ] == 0
            ):
                total_dot_balls += 1

            wicket_count = len(
                parsed[
                    "wickets"
                ]
            )

            total_wickets += (
                wicket_count
            )

            over_wickets += (
                wicket_count
            )

        overs.append(
            {
                "over":
                    over_number,

                "runs":
                    over_runs,

                "balls":
                    over_balls,

                "wickets":
                    over_wickets,

                "deliveries":
                    deliveries,
            }
        )

    return {
        "innings_number":
            innings_number,

        "team":
            team,

        "overs":
            overs,

        "runs":
            total_runs,

        "balls":
            total_balls,

        "wickets":
            total_wickets,

        "boundaries":
            total_boundaries,

        "dot_balls":
            total_dot_balls,
    }


# ============================================================
# Player Extraction
# ============================================================

def extract_players(
    info: dict,
) -> dict:
    """
    Extract players by team from match metadata.
    """

    players = info.get(
        "players",
        {},
    )

    result = {}

    for team, team_players in (
        players.items()
    ):

        result[team] = list(
            team_players
        )

    return result


# ============================================================
# Officials / Registry Information
# ============================================================

def extract_registry(
    info: dict,
) -> dict:
    """
    Extract optional registry information when
    available in the Cricsheet file.
    """

    registry = info.get(
        "registry",
        {},
    )

    return registry


# ============================================================
# Match Metadata
# ============================================================

def extract_match_metadata(
    info: dict,
) -> dict:

    dates = info.get(
        "dates",
        [],
    )

    match_date = None

    if dates:

        match_date = str(
            dates[0]
        )

    event = info.get(
        "event",
        {},
    )

    outcome = info.get(
        "outcome",
        {},
    )

    toss = info.get(
        "toss",
        {},
    )

    teams = info.get(
        "teams",
        [],
    )

    return {

        "match_date":
            match_date,

        "teams":
            teams,

        "venue":
            info.get(
                "venue"
            ),

        "city":
            info.get(
                "city"
            ),

        "gender":
            info.get(
                "gender"
            ),

        "season":
            str(
                info.get(
                    "season"
                )
            )
            if info.get(
                "season"
            ) is not None
            else None,

        "competition":
            event.get(
                "name"
            ),

        "event_match_number":
            event.get(
                "match_number"
            ),

        "toss_winner":
            toss.get(
                "winner"
            ),

        "toss_decision":
            toss.get(
                "decision"
            ),

        "winner":
            outcome.get(
                "winner"
            ),

        "result":
            outcome.get(
                "result"
            ),

        "winner_runs":
            outcome.get(
                "by",
                {},
            ).get(
                "runs"
            ),

        "winner_wickets":
            outcome.get(
                "by",
                {},
            ).get(
                "wickets"
            ),

        "super_over":
            outcome.get(
                "winner"
            ) is not None
            and outcome.get(
                "method"
            ) == "superover",
    }


# ============================================================
# Complete Match Parser
# ============================================================

def parse_match(
    file_path: Path,
) -> dict:

    data = load_match(
        file_path
    )

    info = data.get(
        "info",
        {},
    )

    metadata = extract_match_metadata(
        info
    )

    players = extract_players(
        info
    )

    registry = extract_registry(
        info
    )

    innings = []

    for index, raw_innings in enumerate(
        data.get(
            "innings",
            [],
        ),
        start=1,
    ):

        innings.append(
            parse_innings(
                raw_innings,
                index,
            )
        )

    return {

        "match_id":
            file_path.stem,

        "match_date":
            metadata[
                "match_date"
            ],

        "team1":
            (
                metadata["teams"][0]
                if len(
                    metadata["teams"]
                ) > 0
                else None
            ),

        "team2":
            (
                metadata["teams"][1]
                if len(
                    metadata["teams"]
                ) > 1
                else None
            ),

        "teams":
            metadata[
                "teams"
            ],

        "venue":
            metadata[
                "venue"
            ],

        "city":
            metadata[
                "city"
            ],

        "season":
            metadata[
                "season"
            ],

        "gender":
            metadata[
                "gender"
            ],

        "competition":
            metadata[
                "competition"
            ],

        "event_match_number":
            metadata[
                "event_match_number"
            ],

        "toss_winner":
            metadata[
                "toss_winner"
            ],

        "toss_decision":
            metadata[
                "toss_decision"
            ],

        "winner":
            metadata[
                "winner"
            ],

        "result":
            metadata[
                "result"
            ],

        "winner_runs":
            metadata[
                "winner_runs"
            ],

        "winner_wickets":
            metadata[
                "winner_wickets"
            ],

        "super_over":
            metadata[
                "super_over"
            ],

        "players":
            players,

        "registry":
            registry,

        "innings":
            innings,
    }


# ============================================================
# Parse All Matches
# ============================================================

def extract_all_rich_matches(
    raw_directory: Path = RAW_DATA_DIR,
):

    json_files = sorted(
        raw_directory.glob(
            "*.json"
        )
    )

    if not json_files:

        raise FileNotFoundError(
            "No Cricsheet JSON files found."
        )

    results = []

    for file_path in json_files:

        try:

            match = parse_match(
                file_path
            )

            results.append(
                match
            )

        except Exception as error:

            print(
                f"Skipping "
                f"{file_path.name}: "
                f"{error}"
            )

    return results


# ============================================================
# Main Test
# ============================================================

if __name__ == "__main__":

    matches = (
        extract_all_rich_matches()
    )

    print(
        f"Rich matches parsed: "
        f"{len(matches)}"
    )

    if not matches:
        raise SystemExit

    match = matches[0]

    print()
    print(
        "=========================================="
    )
    print(
        "RICH MATCH PARSER TEST"
    )
    print(
        "=========================================="
    )

    print(
        f"Match ID: "
        f"{match['match_id']}"
    )

    print(
        f"Date: "
        f"{match['match_date']}"
    )

    print(
        f"Teams: "
        f"{match['team1']} vs "
        f"{match['team2']}"
    )

    print(
        f"Venue: "
        f"{match['venue']}"
    )

    print(
        f"Toss: "
        f"{match['toss_winner']} "
        f"({match['toss_decision']})"
    )

    print(
        f"Winner: "
        f"{match['winner']}"
    )

    print()

    print(
        "Players:"
    )

    for team, players in (
        match["players"].items()
    ):

        print(
            f"  {team}: "
            f"{len(players)} players"
        )

        print(
            f"    {players}"
        )

    print()

    print(
        "Innings:"
    )

    for innings in (
        match["innings"]
    ):

        print(
            f"  Innings "
            f"{innings['innings_number']}: "
            f"{innings['team']}"
        )

        print(
            f"    Runs: "
            f"{innings['runs']}"
        )

        print(
            f"    Balls: "
            f"{innings['balls']}"
        )

        print(
            f"    Wickets: "
            f"{innings['wickets']}"
        )

        print(
            f"    Overs: "
            f"{len(innings['overs'])}"
        )

        if innings["overs"]:

            first_over = (
                innings["overs"][0]
            )

            print(
                f"    First over: "
                f"{first_over['over']}"
            )

            print(
                f"    Deliveries: "
                f"{len(first_over['deliveries'])}"
            )

            if first_over[
                "deliveries"
            ]:

                first_delivery = (
                    first_over[
                        "deliveries"
                    ][0]
                )

                print()

                print(
                    "    First delivery:"
                )

                print(
                    f"      Batter: "
                    f"{first_delivery['batter']}"
                )

                print(
                    f"      Bowler: "
                    f"{first_delivery['bowler']}"
                )

                print(
                    f"      Runs: "
                    f"{first_delivery['total_runs']}"
                )

                print(
                    f"      Wickets: "
                    f"{first_delivery['wickets']}"
                )