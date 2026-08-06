from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.team_stats_repository import (
    get_highest_score,
    get_lowest_score,
    get_team_matches,
    get_team_wins,
)


def get_team_statistics(
    db: Session,
    team_id: int,
):
    """
    Calculate statistics for a team.
    """

    matches = get_team_matches(
        db,
        team_id,
    )

    if not matches:
        raise HTTPException(
            status_code=404,
            detail="Team not found or no matches played.",
        )

    matches_played = len(matches)

    wins = get_team_wins(
        db,
        team_id,
    )

    losses = matches_played - wins

    win_percentage = (
        round((wins / matches_played) * 100, 2)
        if matches_played > 0
        else 0.0
    )

    highest_score = get_highest_score(
        db,
        team_id,
    )

    lowest_score = get_lowest_score(
        db,
        team_id,
    )

    return {
        "team_id": team_id,
        "matches": matches_played,
        "wins": wins,
        "losses": losses,
        "win_percentage": win_percentage,
        "highest_score": highest_score or 0,
        "lowest_score": lowest_score or 0,
    }