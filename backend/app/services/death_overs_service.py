from fastapi import HTTPException

from app.repositories.death_overs_repository import (
    get_innings,
    get_death_overs_balls,
)


def get_death_overs(
    db,
    match_id: int,
):
    innings = get_innings(db, match_id)

    if innings is None:
        raise HTTPException(
            status_code=404,
            detail="No innings found.",
        )

    balls = get_death_overs_balls(
        db,
        innings.id,
    )

    if not balls:
        raise HTTPException(
            status_code=404,
            detail="No death-overs data found.",
        )

    runs = sum(ball.runs or 0 for ball in balls)

    wickets = sum(
        1 for ball in balls if ball.is_wicket
    )

    legal_balls = sum(
        1
        for ball in balls
        if ball.extra_type not in ["Wide", "No Ball"]
    )

    boundaries = sum(
        1
        for ball in balls
        if (ball.runs or 0) in [4, 6]
    )

    dot_balls = sum(
        1
        for ball in balls
        if (
            ball.extra_type not in ["Wide", "No Ball"]
            and (ball.runs or 0) == 0
        )
    )

    run_rate = (
        runs / (legal_balls / 6)
        if legal_balls
        else 0
    )

    dot_percentage = (
        dot_balls / legal_balls * 100
        if legal_balls
        else 0
    )

    if run_rate >= 11:
        status = "Excellent"
    elif run_rate >= 9:
        status = "Good"
    elif run_rate >= 7:
        status = "Average"
    else:
        status = "Poor"

    return {
        "match_id": match_id,
        "innings_id": innings.id,
        "runs": runs,
        "wickets": wickets,
        "legal_balls": legal_balls,
        "run_rate": round(run_rate, 2),
        "boundaries": boundaries,
        "dot_balls": dot_balls,
        "dot_ball_percentage": round(
            dot_percentage,
            2,
        ),
        "status": status,
    }