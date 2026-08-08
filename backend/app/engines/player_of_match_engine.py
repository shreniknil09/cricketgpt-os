from sqlalchemy.orm import Session

from app.models.player_match_stats import PlayerMatchStats
from app.models.bowler_match_stats import BowlerMatchStats


def calculate_player_of_match(
    db: Session,
    match_id: int,
):
    """
    Calculate the Player of the Match for a completed match.

    The score combines batting and bowling performance.
    """

    # ---------------------------------
    # Get Batting Statistics
    # ---------------------------------

    batting_records = (
        db.query(PlayerMatchStats)
        .filter(
            PlayerMatchStats.match_id == match_id,
        )
        .all()
    )

    # ---------------------------------
    # Get Bowling Statistics
    # ---------------------------------

    bowling_records = (
        db.query(BowlerMatchStats)
        .filter(
            BowlerMatchStats.match_id == match_id,
        )
        .all()
    )

    # ---------------------------------
    # Store Player Scores
    # ---------------------------------

    player_scores = {}

    # ---------------------------------
    # Calculate Batting Contribution
    # ---------------------------------

    for record in batting_records:

        score = 0.0

        # Runs are the primary batting contribution
        score += record.runs

        # Bonus for boundaries
        score += record.fours * 1.0
        score += record.sixes * 2.0

        player_scores.setdefault(
            record.player_id,
            0.0,
        )

        player_scores[record.player_id] += score

    # ---------------------------------
    # Calculate Bowling Contribution
    # ---------------------------------

    for record in bowling_records:

        score = 0.0

        # Wickets are the primary bowling contribution
        score += record.wickets * 20.0

        # Maiden overs bonus
        score += record.maidens * 5.0

        # Economy bonus
        if record.economy > 0:

            if record.economy <= 5:
                score += 10.0

            elif record.economy <= 7:
                score += 5.0

        player_scores.setdefault(
            record.player_id,
            0.0,
        )

        player_scores[record.player_id] += score

    # ---------------------------------
    # No Statistics
    # ---------------------------------

    if not player_scores:
        return None

    # ---------------------------------
    # Find Highest Score
    # ---------------------------------

    player_id = max(
        player_scores,
        key=player_scores.get,
    )

    score = player_scores[player_id]

    return {
        "match_id": match_id,
        "player_id": player_id,
        "score": round(score, 2),
    }