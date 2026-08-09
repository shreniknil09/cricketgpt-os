from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.batting_phase_repository import (
    get_innings,
    get_balls,
)


def _calculate_phase(balls):
    runs = sum(
        ball.runs or 0
        for ball in balls
    )

    legal_balls = sum(
        1
        for ball in balls
        if ball.extra_type not in [
            "Wide",
            "No Ball",
        ]
    )

    run_rate = (
        runs / (legal_balls / 6)
        if legal_balls
        else 0
    )

    return (
        runs,
        legal_balls,
        round(run_rate, 2),
    )


def get_batting_phase(
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

    ball_rows = get_balls(
        db,
        innings.id,
    )

    if not ball_rows:
        raise HTTPException(
            status_code=404,
            detail="No ball data found.",
        )

    powerplay = []
    middle = []
    death = []

    for ball, over_number in ball_rows:

        if over_number <= 6:
            powerplay.append(ball)

        elif over_number <= 15:
            middle.append(ball)

        else:
            death.append(ball)

    pp = _calculate_phase(powerplay)
    mid = _calculate_phase(middle)
    dth = _calculate_phase(death)

    rates = {
        "Powerplay": pp[2],
        "Middle Overs": mid[2],
        "Death Overs": dth[2],
    }

    best_phase = max(
        rates,
        key=rates.get,
    )

    return {
        "match_id": match_id,
        "innings_id": innings.id,

        "powerplay_runs": pp[0],
        "powerplay_balls": pp[1],
        "powerplay_run_rate": pp[2],

        "middle_overs_runs": mid[0],
        "middle_overs_balls": mid[1],
        "middle_overs_run_rate": mid[2],

        "death_overs_runs": dth[0],
        "death_overs_balls": dth[1],
        "death_overs_run_rate": dth[2],

        "best_phase": best_phase,
    }