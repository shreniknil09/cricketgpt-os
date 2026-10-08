from collections import defaultdict, deque
from pathlib import Path

from app.ml.rich_match_parser import (
    extract_all_rich_matches,
)


# ============================================================
# Configuration
# ============================================================

RECENT_MATCHES = 10
RECENT_PLAYER_MATCHES = 5


# ============================================================
# Helpers
# ============================================================

def safe_divide(
    numerator,
    denominator,
):
    if denominator == 0:
        return 0.0

    return numerator / denominator


def average(values):

    if not values:
        return 0.0

    return sum(values) / len(values)


def phase_from_over(
    over_number,
    total_overs=None,
):
    """
    IPL-style phase classification.

    Powerplay:
        overs 1-6

    Middle:
        overs 7-15

    Death:
        overs 16+

    We use the actual over number supplied by
    Cricsheet.
    """

    if over_number < 6:
        return "powerplay"

    if over_number < 15:
        return "middle"

    return "death"


# ============================================================
# Player State
# ============================================================

class PlayerState:

    def __init__(self):

        self.matches = 0

        # ----------------------------
        # Batting
        # ----------------------------

        self.runs = deque(
            maxlen=RECENT_PLAYER_MATCHES
        )

        self.balls = deque(
            maxlen=RECENT_PLAYER_MATCHES
        )

        self.boundaries = deque(
            maxlen=RECENT_PLAYER_MATCHES
        )

        self.dismissals = deque(
            maxlen=RECENT_PLAYER_MATCHES
        )

        # ----------------------------
        # Bowling
        # ----------------------------

        self.bowling_runs = deque(
            maxlen=RECENT_PLAYER_MATCHES
        )

        self.bowling_balls = deque(
            maxlen=RECENT_PLAYER_MATCHES
        )

        self.wickets = deque(
            maxlen=RECENT_PLAYER_MATCHES
        )

        # ----------------------------
        # Phase batting
        # ----------------------------

        self.phase_runs = defaultdict(
            lambda: deque(
                maxlen=RECENT_MATCHES
            )
        )

        self.phase_balls = defaultdict(
            lambda: deque(
                maxlen=RECENT_MATCHES
            )
        )

        self.phase_boundaries = defaultdict(
            lambda: deque(
                maxlen=RECENT_MATCHES
            )
        )

        # ----------------------------
        # Phase bowling
        # ----------------------------

        self.phase_bowling_runs = defaultdict(
            lambda: deque(
                maxlen=RECENT_MATCHES
            )
        )

        self.phase_bowling_balls = defaultdict(
            lambda: deque(
                maxlen=RECENT_MATCHES
            )
        )

        self.phase_wickets = defaultdict(
            lambda: deque(
                maxlen=RECENT_MATCHES
            )
        )


# ============================================================
# Team State
# ============================================================

class TeamState:

    def __init__(self):

        self.matches = 0
        self.wins = 0

        self.recent_results = deque(
            maxlen=RECENT_MATCHES
        )

        self.recent_runs = deque(
            maxlen=RECENT_MATCHES
        )

        self.recent_balls = deque(
            maxlen=RECENT_MATCHES
        )

        self.recent_wickets = deque(
            maxlen=RECENT_MATCHES
        )


# ============================================================
# Delivery-level Player Statistics
# ============================================================

def calculate_player_match_stats(
    innings,
):

    batting = defaultdict(
        lambda: {
            "runs": 0,
            "balls": 0,
            "boundaries": 0,
            "dismissed": 0,
        }
    )

    bowling = defaultdict(
        lambda: {
            "runs": 0,
            "balls": 0,
            "wickets": 0,
        }
    )

    batting_phase = defaultdict(
        lambda: defaultdict(
            lambda: {
                "runs": 0,
                "balls": 0,
                "boundaries": 0,
            }
        )
    )

    bowling_phase = defaultdict(
        lambda: defaultdict(
            lambda: {
                "runs": 0,
                "balls": 0,
                "wickets": 0,
            }
        )
    )

    for over in innings.get(
        "overs",
        [],
    ):

        over_number = over.get(
            "over",
            0,
        )

        phase = phase_from_over(
            over_number
        )

        for delivery in over.get(
            "deliveries",
            [],
        ):

            batter = delivery.get(
                "batter"
            )

            bowler = delivery.get(
                "bowler"
            )

            batter_runs = delivery.get(
                "batter_runs",
                0,
            )

            total_runs = delivery.get(
                "total_runs",
                0,
            )

            wickets = delivery.get(
                "wickets",
                [],
            )

            # =================================================
            # Batting
            # =================================================

            if batter:

                batting[
                    batter
                ]["runs"] += (
                    batter_runs
                )

                batting[
                    batter
                ]["balls"] += 1

                if batter_runs in (
                    4,
                    6,
                ):

                    batting[
                        batter
                    ]["boundaries"] += 1

                batting_phase[
                    batter
                ][
                    phase
                ]["runs"] += (
                    batter_runs
                )

                batting_phase[
                    batter
                ][
                    phase
                ]["balls"] += 1

                if batter_runs in (
                    4,
                    6,
                ):

                    batting_phase[
                        batter
                    ][
                        phase
                    ]["boundaries"] += 1

            # =================================================
            # Bowling
            # =================================================

            if bowler:

                bowling[
                    bowler
                ]["runs"] += (
                    total_runs
                )

                bowling[
                    bowler
                ]["balls"] += 1

                bowling_phase[
                    bowler
                ][
                    phase
                ]["runs"] += (
                    total_runs
                )

                bowling_phase[
                    bowler
                ][
                    phase
                ]["balls"] += 1

                bowling[
                    bowler
                ]["wickets"] += len(
                    wickets
                )

                bowling_phase[
                    bowler
                ][
                    phase
                ]["wickets"] += len(
                    wickets
                )

            # =================================================
            # Dismissals
            # =================================================

            for wicket in wickets:

                player_out = wicket.get(
                    "player_out"
                )

                if player_out:

                    batting[
                        player_out
                    ]["dismissed"] += 1

    return {
        "batting": batting,
        "bowling": bowling,
        "batting_phase": batting_phase,
        "bowling_phase": bowling_phase,
    }


# ============================================================
# Player Feature Snapshot
# ============================================================

def player_batting_features(
    state,
):

    runs = sum(
        state.runs
    )

    balls = sum(
        state.balls
    )

    boundaries = sum(
        state.boundaries
    )

    dismissals = sum(
        state.dismissals
    )

    return {

        "matches":
            state.matches,

        "runs":
            runs,

        "balls":
            balls,

        "strike_rate":
            round(
                safe_divide(
                    runs * 100,
                    balls,
                ),
                2,
            ),

        "boundary_rate":
            round(
                safe_divide(
                    boundaries,
                    balls,
                ),
                4,
            ),

        "dismissals":
            dismissals,

        "average":
            round(
                safe_divide(
                    runs,
                    dismissals,
                ),
                2,
            ),
    }


def player_bowling_features(
    state,
):

    runs = sum(
        state.bowling_runs
    )

    balls = sum(
        state.bowling_balls
    )

    wickets = sum(
        state.wickets
    )

    return {

        "bowling_balls":
            balls,

        "runs_conceded":
            runs,

        "wickets":
            wickets,

        "economy":
            round(
                safe_divide(
                    runs * 6,
                    balls,
                ),
                2,
            ),

        "wickets_per_ball":
            round(
                safe_divide(
                    wickets,
                    balls,
                ),
                4,
            ),
    }


# ============================================================
# Phase Features
# ============================================================

def calculate_phase_batting_features(
    state,
):

    result = {}

    for phase in (
        "powerplay",
        "middle",
        "death",
    ):

        runs = sum(
            state.phase_runs[
                phase
            ]
        )

        balls = sum(
            state.phase_balls[
                phase
            ]
        )

        boundaries = sum(
            state.phase_boundaries[
                phase
            ]
        )

        result[
            phase
        ] = {

            "runs":
                runs,

            "balls":
                balls,

            "run_rate":
                round(
                    safe_divide(
                        runs * 6,
                        balls,
                    ),
                    2,
                ),

            "boundary_rate":
                round(
                    safe_divide(
                        boundaries,
                        balls,
                    ),
                    4,
                ),
        }

    return result


def calculate_phase_bowling_features(
    state,
):

    result = {}

    for phase in (
        "powerplay",
        "middle",
        "death",
    ):

        runs = sum(
            state.phase_bowling_runs[
                phase
            ]
        )

        balls = sum(
            state.phase_bowling_balls[
                phase
            ]
        )

        wickets = sum(
            state.phase_wickets[
                phase
            ]
        )

        result[
            phase
        ] = {

            "runs_conceded":
                runs,

            "balls":
                balls,

            "economy":
                round(
                    safe_divide(
                        runs * 6,
                        balls,
                    ),
                    2,
                ),

            "wickets":
                wickets,

            "wickets_per_ball":
                round(
                    safe_divide(
                        wickets,
                        balls,
                    ),
                    4,
                ),
        }

    return result


# ============================================================
# Process One Match
# ============================================================

def process_match(
    match,
    player_states,
    team_states,
):

    team1 = match.get(
        "team1"
    )

    team2 = match.get(
        "team2"
    )

    winner = match.get(
        "winner"
    )

    if not team1 or not team2:
        return None

    if winner not in (
        team1,
        team2,
    ):
        return None

    # ========================================================
    # PRE-MATCH PLAYER SNAPSHOT
    # ========================================================

    team1_players = match.get(
        "players",
        {},
    ).get(
        team1,
        [],
    )

    team2_players = match.get(
        "players",
        {},
    ).get(
        team2,
        [],
    )

    team1_features = {}
    team2_features = {}

    for player in team1_players:

        state = player_states[
            player
        ]

        team1_features[
            player
        ] = {

            "batting":
                player_batting_features(
                    state
                ),

            "bowling":
                player_bowling_features(
                    state
                ),

            "batting_phase":
                calculate_phase_batting_features(
                    state
                ),

            "bowling_phase":
                calculate_phase_bowling_features(
                    state
                ),
        }

    for player in team2_players:

        state = player_states[
            player
        ]

        team2_features[
            player
        ] = {

            "batting":
                player_batting_features(
                    state
                ),

            "bowling":
                player_bowling_features(
                    state
                ),

            "batting_phase":
                calculate_phase_batting_features(
                    state
                ),

            "bowling_phase":
                calculate_phase_bowling_features(
                    state
                ),
        }

    # ========================================================
    # TEAM PRE-MATCH SNAPSHOT
    # ========================================================

    team1_state = team_states[
        team1
    ]

    team2_state = team_states[
        team2
    ]

    record = {

        "match_id":
            match.get(
                "match_id"
            ),

        "match_date":
            match.get(
                "match_date"
            ),

        "team1":
            team1,

        "team2":
            team2,

        "winner":
            winner,

        "team1_win":
            1
            if winner == team1
            else 0,

        "team1_matches":
            team1_state.matches,

        "team2_matches":
            team2_state.matches,

        "team1_win_rate":
            round(
                safe_divide(
                    team1_state.wins,
                    team1_state.matches,
                ),
                4,
            )
            if team1_state.matches
            else 0.5,

        "team2_win_rate":
            round(
                safe_divide(
                    team2_state.wins,
                    team2_state.matches,
                ),
                4,
            )
            if team2_state.matches
            else 0.5,

        "team1_players":
            team1_features,

        "team2_players":
            team2_features,
    }

    # ========================================================
    # POST-MATCH UPDATE
    # ========================================================

    team1_state.matches += 1

    team2_state.matches += 1

    team1_won = (
        winner == team1
    )

    team1_state.wins += (
        1
        if team1_won
        else 0
    )

    team2_state.wins += (
        0
        if team1_won
        else 1
    )

    team1_state.recent_results.append(
        1 if team1_won else 0
    )

    team2_state.recent_results.append(
        0 if team1_won else 1
    )

    # ========================================================
    # Process innings
    # ========================================================

    for innings in match.get(
        "innings",
        [],
    ):

        team = innings.get(
            "team"
        )

        if team not in (
            team1,
            team2,
        ):
            continue

        stats = calculate_player_match_stats(
            innings
        )

        # ====================================================
        # Player batting
        # ====================================================

        for player, values in (
            stats["batting"].items()
        ):

            state = player_states[
                player
            ]

            state.matches += 1

            state.runs.append(
                values["runs"]
            )

            state.balls.append(
                values["balls"]
            )

            state.boundaries.append(
                values["boundaries"]
            )

            state.dismissals.append(
                values["dismissed"]
            )

            for phase, phase_values in (
                stats[
                    "batting_phase"
                ][player].items()
            ):

                state.phase_runs[
                    phase
                ].append(
                    phase_values[
                        "runs"
                    ]
                )

                state.phase_balls[
                    phase
                ].append(
                    phase_values[
                        "balls"
                    ]
                )

                state.phase_boundaries[
                    phase
                ].append(
                    phase_values[
                        "boundaries"
                    ]
                )

        # ====================================================
        # Player bowling
        # ====================================================

        for player, values in (
            stats["bowling"].items()
        ):

            state = player_states[
                player
            ]

            state.bowling_runs.append(
                values["runs"]
            )

            state.bowling_balls.append(
                values["balls"]
            )

            state.wickets.append(
                values["wickets"]
            )

            for phase, phase_values in (
                stats[
                    "bowling_phase"
                ][player].items()
            ):

                state.phase_bowling_runs[
                    phase
                ].append(
                    phase_values[
                        "runs"
                    ]
                )

                state.phase_bowling_balls[
                    phase
                ].append(
                    phase_values[
                        "balls"
                    ]
                )

                state.phase_wickets[
                    phase
                ].append(
                    phase_values[
                        "wickets"
                    ]
                )

    return record


# ============================================================
# Build Historical Player Feature Store
# ============================================================

def build_player_phase_features(
    matches,
):

    player_states = defaultdict(
        PlayerState
    )

    team_states = defaultdict(
        TeamState
    )

    records = []

    matches = sorted(
        matches,
        key=lambda match: (
            match.get(
                "match_date",
                "",
            ),
            str(
                match.get(
                    "match_id",
                    "",
                )
            ),
        ),
    )

    for match in matches:

        record = process_match(
            match,
            player_states,
            team_states,
        )

        if record is not None:

            records.append(
                record
            )

    return records


# ============================================================
# Main Test
# ============================================================

if __name__ == "__main__":

    print(
        "Loading rich match data..."
    )

    matches = (
        extract_all_rich_matches()
    )

    print(
        f"Matches loaded: "
        f"{len(matches)}"
    )

    print(
        "Building player and phase features..."
    )

    records = (
        build_player_phase_features(
            matches
        )
    )

    print(
        f"Feature records: "
        f"{len(records)}"
    )

    if records:

        first = records[0]

        print()
        print(
            "=========================================="
        )

        print(
            "PLAYER + PHASE FEATURE TEST"
        )

        print(
            "=========================================="
        )

        print(
            f"Match: "
            f"{first['team1']} vs "
            f"{first['team2']}"
        )

        print(
            f"Date: "
            f"{first['match_date']}"
        )

        print(
            f"Team 1 players: "
            f"{len(first['team1_players'])}"
        )

        print(
            f"Team 2 players: "
            f"{len(first['team2_players'])}"
        )

        if first["team1_players"]:

            player = next(
                iter(
                    first[
                        "team1_players"
                    ]
                )
            )

            print()
            print(
                f"Example player: "
                f"{player}"
            )

            print(
                "Pre-match batting:"
            )

            print(
                first[
                    "team1_players"
                ][player][
                    "batting"
                ]
            )

            print(
                "Pre-match bowling:"
            )

            print(
                first[
                    "team1_players"
                ][player][
                    "bowling"
                ]
            )

            print(
                "Phase batting:"
            )

            print(
                first[
                    "team1_players"
                ][player][
                    "batting_phase"
                ]
            )

            print(
                "Phase bowling:"
            )

            print(
                first[
                    "team1_players"
                ][player][
                    "bowling_phase"
                ]
            )