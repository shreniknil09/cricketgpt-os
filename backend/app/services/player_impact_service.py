from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.match import Match

from app.repositories.player_impact_repository import (
    get_batting_stats,
    get_bowling_stats,
)


def get_player_impact(
    db: Session,
    match_id: int,
):
    """
    Calculate player impact ratings for a match.
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
    # Get Statistics
    # ---------------------------------

    batting_records = get_batting_stats(
        db,
        match_id,
    )

    bowling_records = get_bowling_stats(
        db,
        match_id,
    )

    if not batting_records and not bowling_records:
        raise HTTPException(
            status_code=404,
            detail="No player statistics found for this match.",
        )

    # ---------------------------------
    # Store Player Impact
    # ---------------------------------

    player_impact = {}

    # ---------------------------------
    # Batting Impact
    # ---------------------------------

    for record in batting_records:

        batting_score = 0.0

        batting_score += record.runs
        batting_score += record.fours * 1.0
        batting_score += record.sixes * 2.0

        # Strike-rate bonus
        if record.strike_rate >= 150:
            batting_score += 10.0

        elif record.strike_rate >= 120:
            batting_score += 5.0

        player_impact.setdefault(
            record.player_id,
            {
                "match_id": match_id,
                "player_id": record.player_id,
                "batting_score": 0.0,
                "bowling_score": 0.0,
                "total_impact": 0.0,
            },
        )

        player_impact[
            record.player_id
        ]["batting_score"] += batting_score

    # ---------------------------------
    # Bowling Impact
    # ---------------------------------

    for record in bowling_records:

        bowling_score = 0.0

        bowling_score += (
            record.wickets * 20.0
        )

        bowling_score += (
            record.maidens * 5.0
        )

        # Economy contribution
        if record.economy > 0:

            if record.economy <= 5:
                bowling_score += 10.0

            elif record.economy <= 7:
                bowling_score += 5.0

        player_impact.setdefault(
            record.player_id,
            {
                "match_id": match_id,
                "player_id": record.player_id,
                "batting_score": 0.0,
                "bowling_score": 0.0,
                "total_impact": 0.0,
            },
        )

        player_impact[
            record.player_id
        ]["bowling_score"] += bowling_score

    # ---------------------------------
    # Calculate Total Impact
    # ---------------------------------

    for player in player_impact.values():

        player["total_impact"] = round(
            player["batting_score"]
            + player["bowling_score"],
            2,
        )

        player["batting_score"] = round(
            player["batting_score"],
            2,
        )

        player["bowling_score"] = round(
            player["bowling_score"],
            2,
        )

    # ---------------------------------
    # Return Highest Impact First
    # ---------------------------------

    return sorted(
        player_impact.values(),
        key=lambda player: player["total_impact"],
        reverse=True,
    )
