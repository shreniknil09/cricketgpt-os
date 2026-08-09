from fastapi import HTTPException

from app.repositories.chase_difficulty_repository import (
    get_match,
    get_current_innings,
    get_innings_balls,
)


MAX_BALLS = 120


def get_chase_difficulty(
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

    current_score = sum(
        ball.runs or 0
        for ball in balls
    )

    wickets = sum(
        1
        for ball in balls
        if ball.is_wicket
    )

    legal_balls = sum(
        1
        for ball in balls
        if ball.extra_type not in ["Wide", "No Ball"]
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

    remaining = max(
        target - current_score,
        0,
    )

    balls_remaining = max(
        MAX_BALLS - legal_balls,
        0,
    )

    required_rate = (
        remaining / (balls_remaining / 6)
        if balls_remaining
        else 0
    )

    difficulty = (
        required_rate * 6
        + wickets * 4
    )

    difficulty = max(
        0,
        min(difficulty, 100),
    )

    if difficulty >= 80:
        status = "Extreme"
    elif difficulty >= 60:
        status = "Hard"
    elif difficulty >= 40:
        status = "Moderate"
    else:
        status = "Easy"

    return {
        "match_id": match_id,
        "innings_id": innings.id,
        "runs_remaining": remaining,
        "balls_remaining": balls_remaining,
        "required_run_rate": round(
            required_rate,
            2,
        ),
        "wickets_lost": wickets,
        "difficulty_score": round(
            difficulty,
            2,
        ),
        "difficulty_status": status,
    }