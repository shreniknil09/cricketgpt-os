from fastapi import HTTPException

from app.repositories.pressure_index_repository import (
    get_match,
    get_current_innings,
    get_innings_balls,
)


MAX_BALLS = 120


def get_pressure_index(
    db,
    match_id: int,
):
    match = get_match(db, match_id)

    if match is None:
        raise HTTPException(
            status_code=404,
            detail="Match not found.",
        )

    innings = get_current_innings(
        db,
        match_id,
    )

    if innings is None:
        raise HTTPException(
            status_code=404,
            detail="No innings found.",
        )

    balls = get_innings_balls(
        db,
        innings.id,
    )

    legal_balls = [
        ball
        for ball in balls
        if ball.extra_type not in ["Wide", "No Ball"]
    ]

    current_score = sum(
        ball.runs or 0
        for ball in balls
    )

    wickets = sum(
        1
        for ball in balls
        if ball.is_wicket
    )

    target = getattr(
        match,
        "target",
        None,
    )

    if target is None:
        raise HTTPException(
            status_code=400,
            detail="Target is not available.",
        )

    runs_remaining = max(
        target - current_score,
        0,
    )

    balls_remaining = max(
        MAX_BALLS - len(legal_balls),
        0,
    )

    required_rate = (
        runs_remaining
        / (balls_remaining / 6)
        if balls_remaining
        else 0
    )

    dot_balls = sum(
        1
        for ball in legal_balls
        if (ball.runs or 0) == 0
    )

    dot_percentage = (
        dot_balls
        / len(legal_balls)
        * 100
        if legal_balls
        else 0
    )

    pressure = (
        dot_percentage * 0.4
        + min(required_rate * 5, 50) * 0.4
        + wickets * 2
    )

    pressure = max(
        0,
        min(pressure, 100),
    )

    if pressure >= 80:
        status = "Extreme"
    elif pressure >= 60:
        status = "High"
    elif pressure >= 40:
        status = "Moderate"
    else:
        status = "Low"

    return {
        "match_id": match_id,
        "innings_id": innings.id,
        "dot_ball_percentage": round(
            dot_percentage,
            2,
        ),
        "required_run_rate": round(
            required_rate,
            2,
        ),
        "wickets_lost": wickets,
        "pressure_score": round(
            pressure,
            2,
        ),
        "pressure_status": status,
    }