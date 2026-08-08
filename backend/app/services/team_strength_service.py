from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.team_strength_repository import (
    get_team_batting_stats,
    get_team_bowling_stats,
    get_team_match_results,
)


def get_team_strength(
    db: Session,
    team_id: int,
):
    """
    Calculate a baseline team strength rating.
    """

    batting = get_team_batting_stats(
        db,
        team_id,
    )

    bowling = get_team_bowling_stats(
        db,
        team_id,
    )

    matches = get_team_match_results(
        db,
        team_id,
    )

    if not matches:
        raise HTTPException(
            status_code=404,
            detail="No matches found for this team.",
        )

    # ---------------------------------
    # Batting Strength
    # ---------------------------------

    total_runs = float(
        batting.total_runs or 0
    )

    total_fours = float(
        batting.total_fours or 0
    )

    total_sixes = float(
        batting.total_sixes or 0
    )

    total_balls = float(
        batting.total_balls or 0
    )

    batting_strength = 0.0

    if total_runs > 0:

        batting_strength += min(
            total_runs / 10,
            60,
        )

    batting_strength += min(
        total_fours * 0.5,
        15,
    )

    batting_strength += min(
        total_sixes * 1.0,
        15,
    )

    if total_balls > 0:

        strike_rate = (
            total_runs
            / total_balls
            * 100
        )

        if strike_rate >= 140:
            batting_strength += 10

        elif strike_rate >= 120:
            batting_strength += 7

        elif strike_rate >= 100:
            batting_strength += 4

    batting_strength = min(
        batting_strength,
        100,
    )

    # ---------------------------------
    # Bowling Strength
    # ---------------------------------

    total_wickets = float(
        bowling.total_wickets or 0
    )

    total_runs_given = float(
        bowling.total_runs_given or 0
    )

    total_maidens = float(
        bowling.total_maidens or 0
    )

    bowling_strength = 0.0

    bowling_strength += min(
        total_wickets * 4,
        60,
    )

    bowling_strength += min(
        total_maidens * 3,
        15,
    )

    if total_runs_given > 0:

        wicket_efficiency = (
            total_wickets
            / total_runs_given
            * 100
        )

        bowling_strength += min(
            wicket_efficiency * 5,
            25,
        )

    bowling_strength = min(
        bowling_strength,
        100,
    )

    # ---------------------------------
    # Win Strength
    # ---------------------------------

    completed_matches = [
        match
        for match in matches
        if match.status == "Completed"
    ]

    wins = [
        match
        for match in completed_matches
        if match.winner_id == team_id
    ]

    if completed_matches:

        win_rate = (
            len(wins)
            / len(completed_matches)
            * 100
        )

    else:

        win_rate = 50.0

    win_strength = round(
        win_rate,
        2,
    )

    # ---------------------------------
    # Overall Strength
    # ---------------------------------

    overall_strength = (
        batting_strength * 0.40
        + bowling_strength * 0.40
        + win_strength * 0.20
    )

    # ---------------------------------
    # Return Result
    # ---------------------------------

    return {
        "team_id": team_id,

        "batting_strength": round(
            batting_strength,
            2,
        ),

        "bowling_strength": round(
            bowling_strength,
            2,
        ),

        "win_strength": round(
            win_strength,
            2,
        ),

        "overall_strength": round(
            overall_strength,
            2,
        ),
    }