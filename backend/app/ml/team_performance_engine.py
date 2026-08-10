from collections import defaultdict, deque


# ============================================================
# Configuration
# ============================================================

WINDOW = 10
FORM_WINDOW = 5

INITIAL_ELO = 1500.0
ELO_K_FACTOR = 20.0


# ============================================================
# Match Statistics
# ============================================================

class MatchStats:

    def __init__(self):

        # Batting
        self.runs = 0
        self.legal_balls = 0
        self.boundaries = 0
        self.dot_balls = 0

        # Bowling
        self.wickets = 0
        self.runs_conceded = 0
        self.balls_bowled = 0


# ============================================================
# Team Historical State
# ============================================================

class TeamHistory:

    def __init__(self):

        self.matches = 0
        self.wins = 0

        # Elo rating
        self.elo = INITIAL_ELO

        # Last 10 matches
        self.recent_matches = deque(
            maxlen=WINDOW
        )

        # Last 5 results
        self.recent_results = deque(
            maxlen=FORM_WINDOW
        )


# ============================================================
# Team History Access
# ============================================================

def get_team_history(
    histories,
    team,
):

    if team not in histories:

        histories[team] = TeamHistory()

    return histories[team]


# ============================================================
# Utility Functions
# ============================================================

def calculate_rate(
    runs,
    balls,
):

    if balls <= 0:
        return 0.0

    return runs / (balls / 6.0)


def safe_average(
    values,
):

    if not values:
        return 0.0

    return sum(values) / len(values)


# ============================================================
# Extract One Innings Statistics
# ============================================================

def extract_innings_statistics(
    innings,
):
    """
    Extract batting and bowling statistics
    from one innings.

    Important:
    - Wides are not legal balls.
    - No-balls are not legal balls.
    - Batter runs are separated from total runs.
    """

    stats = MatchStats()

    for over in innings.get(
        "overs",
        [],
    ):

        for delivery in over.get(
            "deliveries",
            [],
        ):

            runs = delivery.get(
                "runs",
                {},
            )

            batter_runs = int(
                runs.get(
                    "batter",
                    0,
                )
            )

            total_runs = int(
                runs.get(
                    "total",
                    0,
                )
            )

            extras = delivery.get(
                "extras",
                {},
            )

            wides = int(
                extras.get(
                    "wides",
                    0,
                )
            )

            no_balls = int(
                extras.get(
                    "noballs",
                    0,
                )
            )

            # --------------------------------
            # Legal delivery
            # --------------------------------

            is_legal = (
                wides == 0
                and no_balls == 0
            )

            if is_legal:

                stats.legal_balls += 1

                stats.balls_bowled += 1

            # --------------------------------
            # Batting
            # --------------------------------

            stats.runs += batter_runs

            if batter_runs in (
                4,
                6,
            ):

                stats.boundaries += 1

            if (
                is_legal
                and total_runs == 0
            ):

                stats.dot_balls += 1

            # --------------------------------
            # Bowling
            # --------------------------------

            stats.runs_conceded += (
                total_runs
            )

            # --------------------------------
            # Wickets
            # --------------------------------

            for wicket in delivery.get(
                "wickets",
                [],
            ):

                kind = str(
                    wicket.get(
                        "kind",
                        "",
                    )
                ).lower()

                excluded = {
                    "retired hurt",
                    "retired not out",
                    "obstructing the field",
                }

                if kind not in excluded:

                    stats.wickets += 1

    return stats


# ============================================================
# Combine Statistics
# ============================================================

def combine_stats(
    stats_list,
):

    combined = MatchStats()

    for stats in stats_list:

        combined.runs += (
            stats.runs
        )

        combined.legal_balls += (
            stats.legal_balls
        )

        combined.boundaries += (
            stats.boundaries
        )

        combined.dot_balls += (
            stats.dot_balls
        )

        combined.wickets += (
            stats.wickets
        )

        combined.runs_conceded += (
            stats.runs_conceded
        )

        combined.balls_bowled += (
            stats.balls_bowled
        )

    return combined


# ============================================================
# Recent Team Statistics
# ============================================================

def get_recent_stats(
    history,
):

    return combine_stats(
        history.recent_matches
    )


# ============================================================
# Calculate Team Features
# ============================================================

def calculate_team_features(
    history,
):
    """
    Calculate only pre-match information.

    No current-match information is used here.
    """

    recent = get_recent_stats(
        history
    )

    matches = history.matches

    # --------------------------------
    # Batting
    # --------------------------------

    run_rate = calculate_rate(
        recent.runs,
        recent.legal_balls,
    )

    boundary_rate = (
        recent.boundaries
        / recent.legal_balls
        if recent.legal_balls
        else 0.0
    )

    dot_ball_rate = (
        recent.dot_balls
        / recent.legal_balls
        if recent.legal_balls
        else 0.0
    )

    average_runs = (
        recent.runs / matches
        if matches
        else 0.0
    )

    # --------------------------------
    # Bowling
    # --------------------------------

    bowling_run_rate = calculate_rate(
        recent.runs_conceded,
        recent.balls_bowled,
    )

    wickets_per_ball = (
        recent.wickets
        / recent.balls_bowled
        if recent.balls_bowled
        else 0.0
    )

    average_wickets = (
        recent.wickets / matches
        if matches
        else 0.0
    )

    # --------------------------------
    # Historical win rate
    # --------------------------------

    win_rate = (
        history.wins / matches
        if matches
        else 0.5
    )

    # --------------------------------
    # Last 5 form
    # --------------------------------

    recent_form = (
        sum(
            history.recent_results
        )
        / len(
            history.recent_results
        )
        if history.recent_results
        else 0.5
    )

    return {

        "average_runs": round(
            average_runs,
            4,
        ),

        "run_rate": round(
            run_rate,
            4,
        ),

        "boundary_rate": round(
            boundary_rate,
            6,
        ),

        "dot_ball_rate": round(
            dot_ball_rate,
            6,
        ),

        "bowling_run_rate": round(
            bowling_run_rate,
            4,
        ),

        "average_wickets": round(
            average_wickets,
            4,
        ),

        "wickets_per_ball": round(
            wickets_per_ball,
            6,
        ),

        "win_rate": round(
            win_rate,
            4,
        ),

        "recent_form": round(
            recent_form,
            4,
        ),

        "elo": round(
            history.elo,
            4,
        ),
    }


# ============================================================
# Elo Rating
# ============================================================

def calculate_elo_probability(
    team1_elo,
    team2_elo,
):

    return 1.0 / (
        1.0
        + 10 ** (
            (
                team2_elo
                - team1_elo
            )
            / 400.0
        )
    )


def update_elo(
    team1_history,
    team2_history,
    team1_won,
):

    expected_team1 = (
        calculate_elo_probability(
            team1_history.elo,
            team2_history.elo,
        )
    )

    actual_team1 = (
        1.0
        if team1_won
        else 0.0
    )

    change = (
        ELO_K_FACTOR
        * (
            actual_team1
            - expected_team1
        )
    )

    team1_history.elo += change

    team2_history.elo -= change


# ============================================================
# Build Innings Map
# ============================================================

def build_innings_map(
    match,
):

    innings_map = defaultdict(
        list
    )

    for innings in match.get(
        "innings",
        [],
    ):

        team = innings.get(
            "team"
        )

        if team:

            innings_map[
                team
            ].append(
                innings
            )

    return innings_map


# ============================================================
# Create Team Match Statistics
# ============================================================

def create_team_match_stats(
    innings_map,
    team,
):
    """
    Creates batting statistics for a team
    and bowling statistics against opponents.
    """

    # --------------------------------
    # Batting
    # --------------------------------

    batting_innings = (
        innings_map.get(
            team,
            [],
        )
    )

    batting_stats = combine_stats(
        [
            extract_innings_statistics(
                innings
            )
            for innings in batting_innings
        ]
    )

    # --------------------------------
    # Bowling
    # --------------------------------

    bowling_stats = MatchStats()

    for opponent, innings_list in (
        innings_map.items()
    ):

        if opponent == team:
            continue

        for innings in innings_list:

            opponent_stats = (
                extract_innings_statistics(
                    innings
                )
            )

            bowling_stats.runs_conceded += (
                opponent_stats.runs
                + sum(
                    delivery.get(
                        "runs",
                        {},
                    ).get(
                        "extras",
                        0,
                    )
                    for over in innings.get(
                        "overs",
                        [],
                    )
                    for delivery in over.get(
                        "deliveries",
                        [],
                    )
                )
            )

            bowling_stats.balls_bowled += (
                opponent_stats.legal_balls
            )

            bowling_stats.wickets += (
                opponent_stats.wickets
            )

    return (
        batting_stats,
        bowling_stats,
    )


# ============================================================
# Update Team History
# ============================================================

def update_team_history(
    history,
    batting_stats,
    bowling_stats,
    won,
):

    history.matches += 1

    if won:

        history.wins += 1

    history.recent_results.append(
        1 if won else 0
    )

    match_stats = MatchStats()

    match_stats.runs = (
        batting_stats.runs
    )

    match_stats.legal_balls = (
        batting_stats.legal_balls
    )

    match_stats.boundaries = (
        batting_stats.boundaries
    )

    match_stats.dot_balls = (
        batting_stats.dot_balls
    )

    match_stats.wickets = (
        bowling_stats.wickets
    )

    match_stats.runs_conceded = (
        bowling_stats.runs_conceded
    )

    match_stats.balls_bowled = (
        bowling_stats.balls_bowled
    )

    history.recent_matches.append(
        match_stats
    )


# ============================================================
# Main Historical Feature Engine
# ============================================================

def build_team_performance_history(
    matches,
):
    """
    Generate leakage-free chronological
    pre-match features.

    For every match:

        1. Read previous team history.
        2. Generate features.
        3. Store current-match target.
        4. Update team statistics.
        5. Update Elo.

    Therefore current-match information is
    NEVER used to generate its own features.
    """

    histories = {}

    records = []

    # --------------------------------
    # Chronological ordering
    # --------------------------------

    matches = sorted(
        matches,
        key=lambda match: (
            match.get(
                "match_date",
                "",
            ),
            match.get(
                "match_id",
                0,
            ),
        ),
    )

    # --------------------------------
    # Process every match
    # --------------------------------

    for match in matches:

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

            continue

        if winner not in {
            team1,
            team2,
        }:

            continue

        # --------------------------------
        # Get team history
        # --------------------------------

        team1_history = (
            get_team_history(
                histories,
                team1,
            )
        )

        team2_history = (
            get_team_history(
                histories,
                team2,
            )
        )

        # --------------------------------
        # PRE-MATCH FEATURES
        # --------------------------------

        team1_features = (
            calculate_team_features(
                team1_history
            )
        )

        team2_features = (
            calculate_team_features(
                team2_history
            )
        )

        # --------------------------------
        # Elo difference
        # --------------------------------

        elo_difference = (
            team1_history.elo
            - team2_history.elo
        )

        # --------------------------------
        # Create training record
        # --------------------------------

        record = {

            "match_id":
                match.get(
                    "match_id"
                ),

            "team1":
                team1,

            "team2":
                team2,

            "match_date":
                match.get(
                    "match_date"
                ),

            "venue":
                match.get(
                    "venue"
                ),

            "toss_winner":
                match.get(
                    "toss_winner"
                ),

            "toss_decision":
                match.get(
                    "toss_decision"
                ),

            # --------------------------------
            # Elo
            # --------------------------------

            "team1_elo":
                round(
                    team1_history.elo,
                    4,
                ),

            "team2_elo":
                round(
                    team2_history.elo,
                    4,
                ),

            "elo_difference":
                round(
                    elo_difference,
                    4,
                ),

            # --------------------------------
            # Batting
            # --------------------------------

            "batting_runs_difference":
                round(
                    team1_features[
                        "average_runs"
                    ]
                    -
                    team2_features[
                        "average_runs"
                    ],
                    4,
                ),

            "run_rate_difference":
                round(
                    team1_features[
                        "run_rate"
                    ]
                    -
                    team2_features[
                        "run_rate"
                    ],
                    4,
                ),

            "boundary_rate_difference":
                round(
                    team1_features[
                        "boundary_rate"
                    ]
                    -
                    team2_features[
                        "boundary_rate"
                    ],
                    6,
                ),

            "dot_ball_rate_difference":
                round(
                    team1_features[
                        "dot_ball_rate"
                    ]
                    -
                    team2_features[
                        "dot_ball_rate"
                    ],
                    6,
                ),

            # --------------------------------
            # Bowling
            # --------------------------------

            "runs_conceded_difference":
                round(
                    team2_features[
                        "bowling_run_rate"
                    ]
                    -
                    team1_features[
                        "bowling_run_rate"
                    ],
                    4,
                ),

            "wickets_difference":
                round(
                    team1_features[
                        "average_wickets"
                    ]
                    -
                    team2_features[
                        "average_wickets"
                    ],
                    4,
                ),

            "bowling_run_rate_difference":
                round(
                    team2_features[
                        "bowling_run_rate"
                    ]
                    -
                    team1_features[
                        "bowling_run_rate"
                    ],
                    4,
                ),

            "wickets_per_ball_difference":
                round(
                    team1_features[
                        "wickets_per_ball"
                    ]
                    -
                    team2_features[
                        "wickets_per_ball"
                    ],
                    6,
                ),

            # --------------------------------
            # Form
            # --------------------------------

            "win_rate_difference":
                round(
                    team1_features[
                        "win_rate"
                    ]
                    -
                    team2_features[
                        "win_rate"
                    ],
                    4,
                ),

            "form_difference":
                round(
                    team1_features[
                        "recent_form"
                    ]
                    -
                    team2_features[
                        "recent_form"
                    ],
                    4,
                ),

            # --------------------------------
            # Target
            # --------------------------------

            "team1_win":
                1
                if winner == team1
                else 0,
        }

        records.append(
            record
        )

        # --------------------------------
        # POST-MATCH UPDATE
        # --------------------------------

        innings_map = (
            build_innings_map(
                match
            )
        )

        (
            team1_batting,
            team1_bowling,
        ) = create_team_match_stats(
            innings_map,
            team1,
        )

        (
            team2_batting,
            team2_bowling,
        ) = create_team_match_stats(
            innings_map,
            team2,
        )

        # --------------------------------
        # Update team 1
        # --------------------------------

        update_team_history(
            team1_history,
            team1_batting,
            team1_bowling,
            winner == team1,
        )

        # --------------------------------
        # Update team 2
        # --------------------------------

        update_team_history(
            team2_history,
            team2_batting,
            team2_bowling,
            winner == team2,
        )

        # --------------------------------
        # Update Elo AFTER match
        # --------------------------------

        update_elo(
            team1_history,
            team2_history,
            winner == team1,
        )

    return records