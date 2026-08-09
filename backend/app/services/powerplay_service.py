from fastapi import HTTPException

from app.repositories.powerplay_repository import (
    get_innings,
    get_powerplay_balls,
)


def get_powerplay(
    db,
    match_id: int,
):
    innings = get_innings(
        db,
        match_id,
    )

    if innings is None:
        raise HTTPException(
            status_code=404,
            detail="No innings found.",
        )

    balls = get_powerplay_balls(
        db,
        innings.id,
    )

    if not balls:
        raise HTTPException(
            status_code=404,
            detail="No powerplay data found.",
        )

    runs = sum(
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
        if ball.extra_type not in [
            "Wide",
            "No Ball",
        ]
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
            ball.extra_type not in [
                "Wide",
                "No Ball",
            ]
            and (ball.runs or 0) == 0
        )
    )

    run_rate = (
        runs / (legal_balls / 6)
        if legal_balls
        else 0
    )

    dot_ball_percentage = (
        dot_balls / legal_balls * 100
        if legal_balls
        else 0
    )

    if run_rate >= 9:
        status = "Excellent"

    elif run_rate >= 7:
        status = "Good"

    elif run_rate >= 5:
        status = "Average"

    else:
        status = "Poor"

    return {
        "match_id": match_id,
        "innings_id": innings.id,

        "runs": runs,
        "wickets": wickets,
        "legal_balls": legal_balls,

        "run_rate": round(
            run_rate,
            2,
        ),

        "boundaries": boundaries,
        "dot_balls": dot_balls,

        "dot_ball_percentage": round(
            dot_ball_percentage,
            2,
        ),

        "status": status,
    }