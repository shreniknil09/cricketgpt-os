from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.player_career_repository import (
    get_batting_career,
    get_bowling_career,
)


def get_player_career(
    db: Session,
    player_id: int,
):
    """
    Calculate the career statistics of a player.
    """

    batting_records = get_batting_career(
        db,
        player_id,
    )

    bowling_records = get_bowling_career(
        db,
        player_id,
    )

    if not batting_records and not bowling_records:
        raise HTTPException(
            status_code=404,
            detail="Player statistics not found.",
        )

    # -------------------------
    # Batting Statistics
    # -------------------------

    matches = len(batting_records)

    runs = sum(record.runs for record in batting_records)
    balls = sum(record.balls for record in batting_records)
    fours = sum(record.fours for record in batting_records)
    sixes = sum(record.sixes for record in batting_records)

    strike_rate = (
        round((runs / balls) * 100, 2)
        if balls > 0
        else 0.0
    )

    # -------------------------
    # Bowling Statistics
    # -------------------------

    wickets = sum(
        record.wickets
        for record in bowling_records
    )

    overs = round(
        sum(record.overs for record in bowling_records),
        1,
    )

    runs_given = sum(
        record.runs_given
        for record in bowling_records
    )

    economy = (
        round(runs_given / overs, 2)
        if overs > 0
        else 0.0
    )

    return {
        "player_id": player_id,
        "matches": matches,
        "runs": runs,
        "balls": balls,
        "fours": fours,
        "sixes": sixes,
        "strike_rate": strike_rate,
        "wickets": wickets,
        "overs": overs,
        "economy": economy,
    }