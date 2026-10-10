import csv
from pathlib import Path

from app.ml.player_phase_features import build_player_phase_features
from app.ml.rich_match_parser import extract_all_rich_matches


OUTPUT_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "ml"
    / "player_match_features_v1.csv"
)


def flatten_player_features(records):
    """Flatten pre-match player snapshots into one row per player per match.

    The batting/bowling aggregates use the rolling windows maintained by
    player_phase_features.py. The team_won label is repeated for each player
    in a match; downstream model evaluation must split/group by match_id to
    prevent players from the same match appearing in both train and test.
    """
    rows = []

    for record in records:
        match_id = record.get("match_id")
        match_date = record.get("match_date")
        team1 = record.get("team1")
        team2 = record.get("team2")
        winner = record.get("winner")

        for team, opponent, team_players in (
            (team1, team2, record.get("team1_players", {})),
            (team2, team1, record.get("team2_players", {})),
        ):
            for player_name, features in team_players.items():
                batting = features.get("batting", {})
                bowling = features.get("bowling", {})
                batting_phase = features.get("batting_phase", {})
                bowling_phase = features.get("bowling_phase", {})

                row = {
                    "match_id": match_id,
                    "match_date": match_date,
                    "team": team,
                    "opponent": opponent,
                    "player_name": player_name,
                    "winner": winner,
                    "team_won": int(winner == team),
                    # This is the number of prior XI appearances tracked by
                    # the engine, not necessarily official appearances.
                    "prior_xi_appearances": batting.get("matches", 0),
                    # These batting/bowling aggregates are rolling-window
                    # values, not career totals.
                    "recent_batting_runs": batting.get("runs", 0),
                    "recent_batting_balls": batting.get("balls", 0),
                    "recent_batting_strike_rate": batting.get("strike_rate", 0.0),
                    "recent_batting_boundary_rate": batting.get("boundary_rate", 0.0),
                    "recent_batting_dismissals": batting.get("dismissals", 0),
                    "recent_batting_average": batting.get("average", 0.0),
                    "recent_bowling_balls": bowling.get("bowling_balls", 0),
                    "recent_bowling_runs_conceded": bowling.get("runs_conceded", 0),
                    "recent_bowling_wickets": bowling.get("wickets", 0),
                    "recent_bowling_economy": bowling.get("economy", 0.0),
                    "recent_bowling_wickets_per_ball": bowling.get("wickets_per_ball", 0.0),
                }

                for phase in ("powerplay", "middle", "death"):
                    bat_phase = batting_phase.get(phase, {})
                    bowl_phase = bowling_phase.get(phase, {})

                    row.update({
                        f"recent_{phase}_batting_runs": bat_phase.get("runs", 0),
                        f"recent_{phase}_batting_balls": bat_phase.get("balls", 0),
                        f"recent_{phase}_batting_run_rate": bat_phase.get("run_rate", 0.0),
                        f"recent_{phase}_batting_boundary_rate": bat_phase.get("boundary_rate", 0.0),
                        f"recent_{phase}_bowling_runs_conceded": bowl_phase.get("runs_conceded", 0),
                        f"recent_{phase}_bowling_balls": bowl_phase.get("balls", 0),
                        f"recent_{phase}_bowling_economy": bowl_phase.get("economy", 0.0),
                        f"recent_{phase}_bowling_wickets": bowl_phase.get("wickets", 0),
                        f"recent_{phase}_bowling_wickets_per_ball": bowl_phase.get("wickets_per_ball", 0.0),
                    })

                rows.append(row)

    return rows


def export_player_features(output_path=OUTPUT_PATH):
    matches = extract_all_rich_matches()
    records = build_player_phase_features(matches)
    rows = flatten_player_features(records)

    if not rows:
        raise ValueError("No player feature rows were generated.")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = list(rows[0].keys())
    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    unique_keys = {
        (row["match_id"], row["team"], row["player_name"])
        for row in rows
    }
    if len(unique_keys) != len(rows):
        raise ValueError("Duplicate match/team/player rows detected.")

    print(f"Matches parsed: {len(matches)}")
    print(f"Valid match feature records: {len(records)}")
    print(f"Player-match rows exported: {len(rows)}")
    print(f"Columns: {len(fieldnames)}")
    print(f"Unique match/team/player keys: {len(unique_keys)}")
    print(f"Output: {output_path}")
    print("Note: team_won is repeated across a match's player rows; split downstream data by match_id.")


if __name__ == "__main__":
    export_player_features()
