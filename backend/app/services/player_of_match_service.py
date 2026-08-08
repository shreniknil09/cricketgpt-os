from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.match import Match

from app.repositories.player_of_match_repository import (
    get_player_of_match_batting,
    get_player_of_match_bowling,
)


def get_player_of_match(
    db: Session,
    match_id: int,
):
    """
    Calculate the Player of the Match
    for a completed match.
    """

    # ---------------------------------
    # Validate Match
    # ---------------------------------

    match = (
        db.query(Match)
        .filter(
            Match.id == match_id,
        )
        .first()
    )

    if match is None:
        raise HTTPException(
            status_code=404,
            detail="Match not found.",
        )

    # ---------------------------------
    # Match should be completed
    # ---------------------------------

    if match.status != "Completed":
        raise HTTPException(
            status_code=400,
            detail="Player of the Match is available only after the match is completed.",
        )

    # ---------------------------------
    # Get Statistics
    # ---------------------------------

    batting_records = get_player_of_match_batting(
        db,
        match_id,
    )

    bowling_records = get_player_of_match_bowling(
        db,
        match_id,
    )

    if not batting_records and not bowling_records:
        raise HTTPException(
            status_code=404,
            detail="No player statistics found for this match.",
        )

    # ---------------------------------
    # Calculate Player Scores
    # ---------------------------------

    player_scores = {}

    # ---------------------------------
    # Batting Contribution
    # ---------------------------------

    for record in batting_records:

        score = 0.0

        score += record.runs
        score += record.fours * 1.0
        score += record.sixes * 2.0

        player_scores.setdefault(
            record.player_id,
            0.0,
        )

        player_scores[record.player_id] += score

    # ---------------------------------
    # Bowling Contribution
    # ---------------------------------

    for record in bowling_records:

        score = 0.0

        score += record.wickets * 20.0
        score += record.maidens * 5.0

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
    # Find Best Player
    # ---------------------------------

    if not player_scores:
        raise HTTPException(
            status_code=404,
            detail="Unable to calculate Player of the Match.",
        )

    player_id = max(
        player_scores,
        key=player_scores.get,
    )

    score = player_scores[player_id]

    # ---------------------------------
    # Return Result
    # ---------------------------------

    return {
        "match_id": match_id,
        "player_id": player_id,
        "score": round(score, 2),
    }