from fastapi import HTTPException

from app.repositories.boundary_repository import (
    get_innings,
    get_innings_balls,
)


def get_boundary_analysis(
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

    if not balls:
        raise HTTPException(
            status_code=404,
            detail="No ball data found.",
        )

    total_runs = sum(
        ball.runs or 0
        for ball in balls
    )

    fours = sum(
        1
        for ball in balls
        if (ball.runs or 0) == 4
    )

    sixes = sum(
        1
        for ball in balls
        if (ball.runs or 0) == 6
    )

    total_boundaries = fours + sixes

    boundary_runs = (
        fours * 4
        + sixes * 6
    )

    boundary_percentage = (
        boundary_runs / total_runs * 100
        if total_runs
        else 0
    )

    if boundary_percentage >= 50:
        status = "Boundary Dominant"
    elif boundary_percentage >= 35:
        status = "High Boundary Dependency"
    elif boundary_percentage >= 20:
        status = "Balanced"
    else:
        status = "Low Boundary Dependency"

    return {
        "match_id": match_id,
        "innings_id": innings.id,
        "fours": fours,
        "sixes": sixes,
        "total_boundaries": total_boundaries,
        "boundary_runs": boundary_runs,
        "boundary_percentage": round(
            boundary_percentage,
            2,
        ),
        "boundary_status": status,
    }