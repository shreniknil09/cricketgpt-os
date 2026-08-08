from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.head_to_head_repository import (
    get_head_to_head_matches,
)


def get_head_to_head(
    db: Session,
    team1_id: int,
    team2_id: int,
):
    """
    Calculate historical head-to-head performance
    between two teams.
    """

    # ---------------------------------
    # Validate Teams
    # ---------------------------------

    if team1_id == team2_id:
        raise HTTPException(
            status_code=400,
            detail="Team 1 and Team 2 must be different.",
        )

    # ---------------------------------
    # Get Matches
    # ---------------------------------

    matches = get_head_to_head_matches(
        db,
        team1_id,
        team2_id,
    )

    if not matches:
        raise HTTPException(
            status_code=404,
            detail="No completed head-to-head matches found.",
        )

    # ---------------------------------
    # Count Wins
    # ---------------------------------

    team1_wins = 0
    team2_wins = 0

    for match in matches:

        if match.winner_id == team1_id:

            team1_wins += 1

        elif match.winner_id == team2_id:

            team2_wins += 1

    # ---------------------------------
    # Win Rates
    # ---------------------------------

    total_matches = len(matches)

    team1_win_rate = (
        team1_wins
        / total_matches
        * 100
    )

    team2_win_rate = (
        team2_wins
        / total_matches
        * 100
    )

    # ---------------------------------
    # Dominant Team
    # ---------------------------------

    if team1_wins > team2_wins:

        dominant_team_id = team1_id

    elif team2_wins > team1_wins:

        dominant_team_id = team2_id

    else:

        dominant_team_id = None

    # ---------------------------------
    # Return
    # ---------------------------------

    return {
        "team1_id": team1_id,
        "team2_id": team2_id,

        "matches": total_matches,

        "team1_wins": team1_wins,
        "team2_wins": team2_wins,

        "team1_win_rate": round(
            team1_win_rate,
            2,
        ),

        "team2_win_rate": round(
            team2_win_rate,
            2,
        ),

        "dominant_team_id": dominant_team_id,
    }