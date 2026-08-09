from fastapi import HTTPException

from app.repositories.required_run_rate_repository import (
    get_match,
    get_current_innings,
    get_innings_balls,
)


MAX_BALLS = 120


def get_required_run_rate(
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

    legal_balls = sum(
        1
        for ball in balls
        if ball.extra_type not in ["Wide", "No Ball"]
    )

    # The target is normally supplied by
    # the previous innings.
    #
    # If your Match model already stores target,
    # that field should be used here.

    target = getattr(
        match,
        "target",
        None,
    )

    if target is None:
        raise HTTPException(
            status_code=400,
            detail="Target is not available for this match.",
        )

    runs_remaining = max(
        target - current_score,
        0,
    )

    balls_remaining = max(
        MAX_BALLS - legal_balls,
        0,
    )

    if balls_remaining > 0:
        required_rate = (
            runs_remaining
            / (balls_remaining / 6)
        )
    else:
        required_rate = 0

    if runs_remaining <= 0:
        status = "Chase Completed"
    elif required_rate <= 6:
        status = "Comfortable"
    elif required_rate <= 8:
        status = "Manageable"
    elif required_rate <= 10:
        status = "Difficult"
    else:
        status = "Very Difficult"

    return {
        "match_id": match_id,
        "innings_id": innings.id,
        "target": target,
        "current_score": current_score,
        "runs_remaining": runs_remaining,
        "balls_remaining": balls_remaining,
        "required_run_rate": round(
            required_rate,
            2,
        ),
        "chase_status": status,
    }