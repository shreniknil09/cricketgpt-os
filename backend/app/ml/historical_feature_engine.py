from collections import defaultdict, deque


class TeamHistory:

    def __init__(self):
        self.matches = 0
        self.wins = 0
        self.runs = []
        self.run_rates = []
        self.boundary_rates = []
        self.dot_ball_rates = []
        self.recent_results = deque(
            maxlen=5
        )


def _get_team_history(
    histories,
    team,
):
    if team not in histories:
        histories[team] = TeamHistory()

    return histories[team]


def _get_h2h_key(
    team1,
    team2,
):
    return tuple(
        sorted(
            [team1, team2]
        )
    )


def _calculate_recent_form(
    history: TeamHistory,
):
    if not history.recent_results:
        return 0.5

    return (
        sum(history.recent_results)
        / len(history.recent_results)
    )


def _calculate_strength(
    history: TeamHistory,
):
    if history.matches == 0:
        return 0.5

    win_rate = (
        history.wins
        / history.matches
    )

    average_run_rate = (
        sum(history.run_rates)
        / len(history.run_rates)
        if history.run_rates
        else 0
    )

    average_boundary_rate = (
        sum(history.boundary_rates)
        / len(history.boundary_rates)
        if history.boundary_rates
        else 0
    )

    average_dot_rate = (
        sum(history.dot_ball_rates)
        / len(history.dot_ball_rates)
        if history.dot_ball_rates
        else 0
    )

    strength = (
        win_rate * 0.50
        + min(
            average_run_rate / 15,
            1,
        ) * 0.25
        + min(
            average_boundary_rate * 5,
            1,
        ) * 0.15
        + min(
            average_dot_rate * 2,
            1,
        ) * 0.10
    )

    return round(
        strength,
        4,
    )


def _calculate_venue_advantage(
    venue_history,
    team,
    opponent,
):
    key = (
        venue_history
        .get(venue_history_key(venue_history, team))
    )

    if not key:
        return 0.0

    matches = key["matches"]

    if matches == 0:
        return 0.0

    team_win_rate = (
        key["wins"] / matches
    )

    return round(
        team_win_rate - 0.5,
        4,
    )


def venue_history_key(
    venue_history,
    team,
):
    return (
        id(venue_history),
        team,
    )


def build_historical_features(
    matches,
):
    """
    Build pre-match features.

    IMPORTANT:
    Every feature for a match is calculated
    using only matches BEFORE the current match.
    """

    histories = {}

    h2h_history = defaultdict(
        lambda: {
            "matches": 0,
            "team1_wins": 0,
        }
    )

    venue_history = {}

    records = []

    for match in matches:

        team1 = match["team1"]
        team2 = match["team2"]
        venue = match.get("venue")

        team1_history = _get_team_history(
            histories,
            team1,
        )

        team2_history = _get_team_history(
            histories,
            team2,
        )

        # -----------------------------
        # Team strength
        # -----------------------------

        team1_strength = (
            _calculate_strength(
                team1_history
            )
        )

        team2_strength = (
            _calculate_strength(
                team2_history
            )
        )

        # -----------------------------
        # Recent form
        # -----------------------------

        team1_form = (
            _calculate_recent_form(
                team1_history
            )
        )

        team2_form = (
            _calculate_recent_form(
                team2_history
            )
        )

        # -----------------------------
        # Head-to-head
        # -----------------------------

        h2h_key = _get_h2h_key(
            team1,
            team2,
        )

        h2h = h2h_history[
            h2h_key
        ]

        if h2h["matches"] > 0:

            h2h_team1_rate = (
                h2h["team1_wins"]
                / h2h["matches"]
            )

            h2h_advantage = (
                h2h_team1_rate - 0.5
            )

        else:

            h2h_advantage = 0.0

        # -----------------------------
        # Venue advantage
        # -----------------------------

        venue_team1 = (
            venue_history.get(
                (venue, team1),
                {
                    "matches": 0,
                    "wins": 0,
                },
            )
        )

        venue_team2 = (
            venue_history.get(
                (venue, team2),
                {
                    "matches": 0,
                    "wins": 0,
                },
            )
        )

        team1_venue_rate = (
            venue_team1["wins"]
            / venue_team1["matches"]
            if venue_team1["matches"]
            else 0.5
        )

        team2_venue_rate = (
            venue_team2["wins"]
            / venue_team2["matches"]
            if venue_team2["matches"]
            else 0.5
        )

        venue_advantage = (
            team1_venue_rate
            - team2_venue_rate
        )

        # -----------------------------
        # Momentum
        # -----------------------------

        momentum = (
            team1_form
            - team2_form
        )

        # -----------------------------
        # Pressure index
        # -----------------------------

        pressure_index = abs(
            momentum
        )

        # -----------------------------
        # Historical run rate
        # -----------------------------

        team1_rr = (
            sum(team1_history.run_rates)
            / len(team1_history.run_rates)
            if team1_history.run_rates
            else 0
        )

        team2_rr = (
            sum(team2_history.run_rates)
            / len(team2_history.run_rates)
            if team2_history.run_rates
            else 0
        )

        average_run_rate = (
            team1_rr + team2_rr
        ) / 2

        # -----------------------------
        # Match impact
        # -----------------------------

        match_impact = (
            team1_strength
            - team2_strength
        )

        # -----------------------------
        # Target
        # -----------------------------

        if match["winner"] == team1:

            team1_win = 1

        elif match["winner"] == team2:

            team1_win = 0

        else:

            continue

        # -----------------------------
        # Build record
        # -----------------------------

        record = {
            "match_id":
                match["match_id"],

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

            "team1_strength":
                team1_strength,

            "team2_strength":
                team2_strength,

            "team1_form":
                team1_form,

            "team2_form":
                team2_form,

            # Player-level historical
            # feature is not yet available
            # from the current pipeline.
            "team1_player_form":
                0.0,

            "team2_player_form":
                0.0,

            "venue_advantage":
                round(
                    venue_advantage,
                    4,
                ),

            "head_to_head_advantage":
                round(
                    h2h_advantage,
                    4,
                ),

            "momentum":
                round(
                    momentum,
                    4,
                ),

            "pressure_index":
                round(
                    pressure_index,
                    4,
                ),

            "run_rate":
                round(
                    average_run_rate,
                    4,
                ),

            # These are match-state features
            # and are not known pre-match.
            "required_run_rate":
                0.0,

            "chase_difficulty":
                0.0,

            "match_impact":
                round(
                    match_impact,
                    4,
                ),

            "team1_win":
                team1_win,
        }

        records.append(record)

        # =================================
        # UPDATE HISTORY AFTER THE MATCH
        # =================================

        team1_won = (
            match["winner"] == team1
        )

        team2_won = (
            match["winner"] == team2
        )

        # Team 1
        team1_history.matches += 1

        if team1_won:
            team1_history.wins += 1
            team1_history.recent_results.append(
                1
            )
        else:
            team1_history.recent_results.append(
                0
            )

        # Team 2
        team2_history.matches += 1

        if team2_won:
            team2_history.wins += 1
            team2_history.recent_results.append(
                1
            )
        else:
            team2_history.recent_results.append(
                0
            )

        # We don't currently have innings-level
        # rates in this match object, so use the
        # existing match-level run rate if present.
        overall_run_rate = (
            match.get(
                "overall_run_rate"
            )
        )

        if overall_run_rate is not None:

            team1_history.run_rates.append(
                overall_run_rate
            )

            team2_history.run_rates.append(
                overall_run_rate
            )

        # H2H update
        h2h["matches"] += 1

        if team1_won:
            h2h["team1_wins"] += 1

        # Venue update
        if venue:

            team1_key = (
                venue,
                team1,
            )

            team2_key = (
                venue,
                team2,
            )

            if team1_key not in venue_history:
                venue_history[
                    team1_key
                ] = {
                    "matches": 0,
                    "wins": 0,
                }

            if team2_key not in venue_history:
                venue_history[
                    team2_key
                ] = {
                    "matches": 0,
                    "wins": 0,
                }

            venue_history[
                team1_key
            ]["matches"] += 1

            venue_history[
                team2_key
            ]["matches"] += 1

            if team1_won:

                venue_history[
                    team1_key
                ]["wins"] += 1

            else:

                venue_history[
                    team2_key
                ]["wins"] += 1

    return records