from fastapi import HTTPException

from app.repositories.dot_ball_repository import (
    get_innings,
    get_innings_balls,
)


def get_dot_ball_analysis(
    db,
    match_id: int,
):
    innings = get_innings(db, match_id)

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

    if not legal_balls:
        raise HTTPException(
            status_code=400,
            detail="No legal deliveries available.",
        )

    dot_balls = sum(
        1
        for ball in legal_balls
        if (ball.runs or 0) == 0
    )

    percentage = (
        dot_balls
        / len(legal_balls)
        * 100
    )

    if percentage >= 45:
        pressure = "Very High"
    elif percentage >= 35:
        pressure = "High"
    elif percentage >= 25:
        pressure = "Moderate"
    else:
        pressure = "Low"

    return {
        "match_id": match_id,
        "innings_id": innings.id,
        "dot_balls": dot_balls,
        "legal_balls": len(legal_balls),
        "dot_ball_percentage": round(
            percentage,
            2,
        ),
        "pressure_level": pressure,
    }