from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.bowling_phase_repository import (
    get_innings,
    get_phase_balls,
)


def _calculate_phase(rows):
    runs = sum(
        ball.runs or 0
        for ball, _ in rows
    )

    wickets = sum(
        1
        for ball, _ in rows
        if ball.is_wicket
    )

    legal_balls = sum(
        1
        for ball, _ in rows
        if ball.extra_type not in [
            "Wide",
            "No Ball",
        ]
    )

    economy = (
        runs / (legal_balls / 6)
        if legal_balls
        else 0
    )

    return (
        runs,
        wickets,
        round(economy, 2),
    )


def get_bowling_phase(
    db: Session,
    match_id: int,
):
    innings = get_innings(
        db,
        match_id,
    )

    if innings is None:
        raise HTTPException(
            status_code=404,
            detail="No innings found for this match.",
        )

    powerplay_rows = get_phase_balls(
        db,
        innings.id,
        1,
        6,
    )

    middle_rows = get_phase_balls(
        db,
        innings.id,
        7,
        15,
    )

    death_rows = get_phase_balls(
        db,
        innings.id,
        16,
        20,
    )

    powerplay = _calculate_phase(
        powerplay_rows
    )

    middle = _calculate_phase(
        middle_rows
    )

    death = _calculate_phase(
        death_rows
    )

    economies = {
        "Powerplay": powerplay[2],
        "Middle Overs": middle[2],
        "Death Overs": death[2],
    }

    # Lowest economy = best bowling phase
    best_phase = min(
        economies,
        key=economies.get,
    )

    return {
        "match_id": match_id,
        "innings_id": innings.id,

        "powerplay_runs_given": powerplay[0],
        "powerplay_wickets": powerplay[1],
        "powerplay_economy": powerplay[2],

        "middle_overs_runs_given": middle[0],
        "middle_overs_wickets": middle[1],
        "middle_overs_economy": middle[2],

        "death_overs_runs_given": death[0],
        "death_overs_wickets": death[1],
        "death_overs_economy": death[2],

        "best_phase": best_phase,
    }