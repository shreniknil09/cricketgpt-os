from collections import defaultdict, deque


# ============================================================
# V4 FEATURE ENGINE
# ============================================================

WINDOW_10 = 10
WINDOW_5 = 5

INITIAL_ELO = 1500.0
ELO_K_FACTOR = 20.0


# ============================================================
# Team State
# ============================================================

class TeamState:

    def __init__(self):

        self.matches = 0
        self.wins = 0

        # Elo
        self.elo = INITIAL_ELO

        # Recent results
        self.results_5 = deque(
            maxlen=WINDOW_5
        )

        self.results_10 = deque(
            maxlen=WINDOW_10
        )

        # Recent batting
        self.runs_10 = deque(
            maxlen=WINDOW_10
        )

        self.balls_10 = deque(
            maxlen=WINDOW_10
        )

        self.boundaries_10 = deque(
            maxlen=WINDOW_10
        )

        # Recent bowling
        self.runs_conceded_10 = deque(
            maxlen=WINDOW_10
        )

        self.wickets_10 = deque(
            maxlen=WINDOW_10
        )

        self.bowling_balls_10 = deque(
            maxlen=WINDOW_10
        )

        # Head-to-head
        self.head_to_head = defaultdict(
            lambda: {
                "matches": 0,
                "wins": 0,
            }
        )

        # Venue history
        self.venue_history = defaultdict(
            lambda: {
                "matches": 0,
                "wins": 0,
            }
        )


# ============================================================
# Helpers
# ============================================================

def get_team_state(
    states,
    team,
):

    if team not in states:
        states[team] = TeamState()

    return states[team]


def safe_divide(
    numerator,
    denominator,
):

    if denominator == 0:
        return 0.0

    return numerator / denominator


def calculate_run_rate(
    runs,
    balls,
):

    return safe_divide(
        runs,
        balls / 6.0,
    )


def average(
    values,
):

    if not values:
        return 0.0

    return sum(values) / len(values)


# ============================================================
# Extract Innings Statistics
# ============================================================

def extract_innings_stats(
    innings,
):

    runs = 0
    balls = 0
    boundaries = 0
    dot_balls = 0

    wickets = 0
    runs_conceded = 0
    bowling_balls = 0

    for over in innings.get(
        "overs",
        [],
    ):

        for delivery in over.get(
            "deliveries",
            [],
        ):

            delivery_runs = delivery.get(
                "runs",
                {},
            )

            batter_runs = int(
                delivery_runs.get(
                    "batter",
                    0,
                )
            )

            total_runs = int(
                delivery_runs.get(
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

            legal_delivery = (
                wides == 0
                and no_balls == 0
            )

            # ----------------------------
            # Batting
            # ----------------------------

            runs += batter_runs

            if batter_runs in (
                4,
                6,
            ):
                boundaries += 1

            if (
                legal_delivery
                and total_runs == 0
            ):
                dot_balls += 1

            # ----------------------------
            # Bowling
            # ----------------------------

            runs_conceded += total_runs

            if legal_delivery:
                balls += 1
                bowling_balls += 1

            # ----------------------------
            # Wickets
            # ----------------------------

            for wicket in delivery.get(
                "wickets",
                [],
            ):

                wicket_kind = str(
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

                if wicket_kind not in excluded:
                    wickets += 1

    return {
        "runs": runs,
        "balls": balls,
        "boundaries": boundaries,
        "dot_balls": dot_balls,
        "wickets": wickets,
        "runs_conceded": runs_conceded,
        "bowling_balls": bowling_balls,
    }


# ============================================================
# Extract Match Team Statistics
# ============================================================

def extract_match_statistics(
    match,
):

    innings_by_team = defaultdict(list)

    for innings in match.get(
        "innings",
        [],
    ):

        team = innings.get(
            "team"
        )

        if team:
            innings_by_team[
                team
            ].append(
                innings
            )

    team_stats = {}

    for team, innings_list in (
        innings_by_team.items()
    ):

        combined = {
            "runs": 0,
            "balls": 0,
            "boundaries": 0,
            "dot_balls": 0,
            "wickets": 0,
            "runs_conceded": 0,
            "bowling_balls": 0,
        }

        for innings in innings_list:

            stats = extract_innings_stats(
                innings
            )

            for key in combined:

                combined[key] += (
                    stats[key]
                )

        team_stats[team] = combined

    # --------------------------------
    # Bowling statistics
    # --------------------------------

    teams = list(
        innings_by_team.keys()
    )

    for team in teams:

        if team not in team_stats:
            continue

        bowling_runs = 0
        bowling_balls = 0
        bowling_wickets = 0

        for opponent in teams:

            if opponent == team:
                continue

            opponent_stats = (
                team_stats[opponent]
            )

            bowling_runs += (
                opponent_stats[
                    "runs"
                ]
            )

            bowling_balls += (
                opponent_stats[
                    "balls"
                ]
            )

            bowling_wickets += (
                opponent_stats[
                    "wickets"
                ]
            )

        team_stats[team][
            "runs_conceded"
        ] = bowling_runs

        team_stats[team][
            "bowling_balls"
        ] = bowling_balls

        team_stats[team][
            "bowling_wickets"
        ] = bowling_wickets

    return team_stats


# ============================================================
# Elo
# ============================================================

def elo_probability(
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
    team1,
    team2,
    team1_won,
):

    expected = elo_probability(
        team1.elo,
        team2.elo,
    )

    actual = (
        1.0
        if team1_won
        else 0.0
    )

    change = (
        ELO_K_FACTOR
        * (
            actual
            - expected
        )
    )

    team1.elo += change
    team2.elo -= change


# ============================================================
# Recent Form
# ============================================================

def calculate_recent_form(
    results,
):

    if not results:
        return 0.5

    return safe_divide(
        sum(results),
        len(results),
    )


# ============================================================
# Historical Win Rate
# ============================================================

def calculate_win_rate(
    state,
):

    if state.matches == 0:
        return 0.5

    return safe_divide(
        state.wins,
        state.matches,
    )


# ============================================================
# Recent Batting Features
# ============================================================

def calculate_batting_features(
    state,
):

    total_runs = sum(
        state.runs_10
    )

    total_balls = sum(
        state.balls_10
    )

    total_boundaries = sum(
        state.boundaries_10
    )

    return {

        "run_rate":
            calculate_run_rate(
                total_runs,
                total_balls,
            ),

        "boundary_rate":
            safe_divide(
                total_boundaries,
                total_balls,
            ),
    }


# ============================================================
# Recent Bowling Features
# ============================================================

def calculate_bowling_features(
    state,
):

    runs_conceded = sum(
        state.runs_conceded_10
    )

    wickets = sum(
        state.wickets_10
    )

    balls = sum(
        state.bowling_balls_10
    )

    return {

        "bowling_run_rate":
            calculate_run_rate(
                runs_conceded,
                balls,
            ),

        "wickets_per_ball":
            safe_divide(
                wickets,
                balls,
            ),

        "wickets_per_match":
            average(
                state.wickets_10
            ),
    }


# ============================================================
# Head-to-Head
# ============================================================

def calculate_h2h(
    team_state,
    opponent,
):

    record = team_state.head_to_head[
        opponent
    ]

    if record["matches"] == 0:
        return 0.0

    return (
        record["wins"]
        / record["matches"]
    )


# ============================================================
# Venue Advantage
# ============================================================

def calculate_venue_form(
    team_state,
    venue,
):

    if not venue:
        return 0.5

    record = team_state.venue_history[
        venue
    ]

    if record["matches"] == 0:
        return 0.5

    return (
        record["wins"]
        / record["matches"]
    )


# ============================================================
# Build V4 Dataset
# ============================================================

def build_v4_features(
    matches,
):
    """
    Generate chronological V4 features.

    Features for a match are calculated BEFORE
    updating the team histories with that match.

    This prevents target leakage.
    """

    states = {}

    records = []

    # --------------------------------
    # Sort chronologically
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
    # Process matches
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

        venue = match.get(
            "venue"
        )

        if not team1 or not team2:
            continue

        if winner not in {
            team1,
            team2,
        }:
            continue

        team1_state = (
            get_team_state(
                states,
                team1,
            )
        )

        team2_state = (
            get_team_state(
                states,
                team2,
            )
        )

        # ========================================
        # PRE-MATCH FEATURES
        # ========================================

        team1_batting = (
            calculate_batting_features(
                team1_state
            )
        )

        team2_batting = (
            calculate_batting_features(
                team2_state
            )
        )

        team1_bowling = (
            calculate_bowling_features(
                team1_state
            )
        )

        team2_bowling = (
            calculate_bowling_features(
                team2_state
            )
        )

        team1_form_5 = (
            calculate_recent_form(
                team1_state.results_5
            )
        )

        team2_form_5 = (
            calculate_recent_form(
                team2_state.results_5
            )
        )

        team1_form_10 = (
            calculate_recent_form(
                team1_state.results_10
            )
        )

        team2_form_10 = (
            calculate_recent_form(
                team2_state.results_10
            )
        )

        team1_win_rate = (
            calculate_win_rate(
                team1_state
            )
        )

        team2_win_rate = (
            calculate_win_rate(
                team2_state
            )
        )

        team1_h2h = (
            calculate_h2h(
                team1_state,
                team2,
            )
        )

        team2_h2h = (
            calculate_h2h(
                team2_state,
                team1,
            )
        )

        team1_venue = (
            calculate_venue_form(
                team1_state,
                venue,
            )
        )

        team2_venue = (
            calculate_venue_form(
                team2_state,
                venue,
            )
        )

        elo_difference = (
            team1_state.elo
            - team2_state.elo
        )

        # ========================================
        # V4 RECORD
        # ========================================

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
                venue,

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
                    team1_state.elo,
                    4,
                ),

            "team2_elo":
                round(
                    team2_state.elo,
                    4,
                ),

            "elo_difference":
                round(
                    elo_difference,
                    4,
                ),

            # --------------------------------
            # Recent Form
            # --------------------------------

            "team1_form_5":
                round(
                    team1_form_5,
                    4,
                ),

            "team2_form_5":
                round(
                    team2_form_5,
                    4,
                ),

            "form_5_difference":
                round(
                    team1_form_5
                    - team2_form_5,
                    4,
                ),

            "team1_form_10":
                round(
                    team1_form_10,
                    4,
                ),

            "team2_form_10":
                round(
                    team2_form_10,
                    4,
                ),

            "form_10_difference":
                round(
                    team1_form_10
                    - team2_form_10,
                    4,
                ),

            # --------------------------------
            # Win Rate
            # --------------------------------

            "team1_win_rate":
                round(
                    team1_win_rate,
                    4,
                ),

            "team2_win_rate":
                round(
                    team2_win_rate,
                    4,
                ),

            "win_rate_difference":
                round(
                    team1_win_rate
                    - team2_win_rate,
                    4,
                ),

            # --------------------------------
            # Batting
            # --------------------------------

            "team1_run_rate":
                round(
                    team1_batting[
                        "run_rate"
                    ],
                    4,
                ),

            "team2_run_rate":
                round(
                    team2_batting[
                        "run_rate"
                    ],
                    4,
                ),

            "run_rate_difference":
                round(
                    team1_batting[
                        "run_rate"
                    ]
                    -
                    team2_batting[
                        "run_rate"
                    ],
                    4,
                ),

            "boundary_rate_difference":
                round(
                    team1_batting[
                        "boundary_rate"
                    ]
                    -
                    team2_batting[
                        "boundary_rate"
                    ],
                    6,
                ),

            # --------------------------------
            # Bowling
            # --------------------------------

            "team1_bowling_run_rate":
                round(
                    team1_bowling[
                        "bowling_run_rate"
                    ],
                    4,
                ),

            "team2_bowling_run_rate":
                round(
                    team2_bowling[
                        "bowling_run_rate"
                    ],
                    4,
                ),

            "bowling_run_rate_difference":
                round(
                    team2_bowling[
                        "bowling_run_rate"
                    ]
                    -
                    team1_bowling[
                        "bowling_run_rate"
                    ],
                    4,
                ),

            "wickets_difference":
                round(
                    team1_bowling[
                        "wickets_per_match"
                    ]
                    -
                    team2_bowling[
                        "wickets_per_match"
                    ],
                    4,
                ),

            "wickets_per_ball_difference":
                round(
                    team1_bowling[
                        "wickets_per_ball"
                    ]
                    -
                    team2_bowling[
                        "wickets_per_ball"
                    ],
                    6,
                ),

            # --------------------------------
            # Head-to-head
            # --------------------------------

            "team1_h2h_win_rate":
                round(
                    team1_h2h,
                    4,
                ),

            "team2_h2h_win_rate":
                round(
                    team2_h2h,
                    4,
                ),

            "head_to_head_difference":
                round(
                    team1_h2h
                    - team2_h2h,
                    4,
                ),

            # --------------------------------
            # Venue
            # --------------------------------

            "team1_venue_win_rate":
                round(
                    team1_venue,
                    4,
                ),

            "team2_venue_win_rate":
                round(
                    team2_venue,
                    4,
                ),

            "venue_advantage":
                round(
                    team1_venue
                    - team2_venue,
                    4,
                ),

            # --------------------------------
            # Experience
            # --------------------------------

            "team1_matches":
                team1_state.matches,

            "team2_matches":
                team2_state.matches,

            "experience_difference":
                (
                    team1_state.matches
                    - team2_state.matches
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

        # ========================================
        # POST-MATCH UPDATE
        # ========================================

        match_stats = (
            extract_match_statistics(
                match
            )
        )

        team1_stats = (
            match_stats.get(
                team1,
                {},
            )
        )

        team2_stats = (
            match_stats.get(
                team2,
                {},
            )
        )

        # --------------------------------
        # Team 1 update
        # --------------------------------

        team1_state.matches += 1

        if winner == team1:
            team1_state.wins += 1

        team1_state.results_5.append(
            1
            if winner == team1
            else 0
        )

        team1_state.results_10.append(
            1
            if winner == team1
            else 0
        )

        team1_state.runs_10.append(
            team1_stats.get(
                "runs",
                0,
            )
        )

        team1_state.balls_10.append(
            team1_stats.get(
                "balls",
                0,
            )
        )

        team1_state.boundaries_10.append(
            team1_stats.get(
                "boundaries",
                0,
            )
        )

        team1_state.runs_conceded_10.append(
            team1_stats.get(
                "runs_conceded",
                0,
            )
        )

        team1_state.wickets_10.append(
            team1_stats.get(
                "bowling_wickets",
                0,
            )
        )

        team1_state.bowling_balls_10.append(
            team1_stats.get(
                "bowling_balls",
                0,
            )
        )

        # --------------------------------
        # Team 2 update
        # --------------------------------

        team2_state.matches += 1

        if winner == team2:
            team2_state.wins += 1

        team2_state.results_5.append(
            1
            if winner == team2
            else 0
        )

        team2_state.results_10.append(
            1
            if winner == team2
            else 0
        )

        team2_state.runs_10.append(
            team2_stats.get(
                "runs",
                0,
            )
        )

        team2_state.balls_10.append(
            team2_stats.get(
                "balls",
                0,
            )
        )

        team2_state.boundaries_10.append(
            team2_stats.get(
                "boundaries",
                0,
            )
        )

        team2_state.runs_conceded_10.append(
            team2_stats.get(
                "runs_conceded",
                0,
            )
        )

        team2_state.wickets_10.append(
            team2_stats.get(
                "bowling_wickets",
                0,
            )
        )

        team2_state.bowling_balls_10.append(
            team2_stats.get(
                "bowling_balls",
                0,
            )
        )

        # --------------------------------
        # H2H update
        # --------------------------------

        team1_state.head_to_head[
            team2
        ]["matches"] += 1

        team2_state.head_to_head[
            team1
        ]["matches"] += 1

        if winner == team1:

            team1_state.head_to_head[
                team2
            ]["wins"] += 1

        else:

            team2_state.head_to_head[
                team1
            ]["wins"] += 1

        # --------------------------------
        # Venue update
        # --------------------------------

        if venue:

            team1_state.venue_history[
                venue
            ]["matches"] += 1

            team2_state.venue_history[
                venue
            ]["matches"] += 1

            if winner == team1:

                team1_state.venue_history[
                    venue
                ]["wins"] += 1

            else:

                team2_state.venue_history[
                    venue
                ]["wins"] += 1

        # --------------------------------
        # Elo update AFTER match
        # --------------------------------

        update_elo(
            team1_state,
            team2_state,
            winner == team1,
        )

    return records