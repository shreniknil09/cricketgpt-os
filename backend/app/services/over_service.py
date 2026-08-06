from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.innings import Innings
from app.repositories.over_repository import (
    create_over,
    get_all_overs,
    get_innings_overs,
    get_over_by_id,
)


def get_overs(db: Session):
    return get_all_overs(db)


def get_single_over(
    db: Session,
    over_id: int,
):
    over = get_over_by_id(db, over_id)

    if over is None:
        raise HTTPException(
            status_code=404,
            detail="Over not found.",
        )

    return over


def add_over(
    db: Session,
    over,
):
    # Rule 1: Innings must exist
    innings = (
        db.query(Innings)
        .filter(Innings.id == over.innings_id)
        .first()
    )

    if innings is None:
        raise HTTPException(
            status_code=404,
            detail="Innings not found.",
        )

    # Rule 2: Maximum 20 overs
    existing_overs = get_innings_overs(
        db,
        over.innings_id,
    )

    if len(existing_overs) >= 20:
        raise HTTPException(
            status_code=400,
            detail="Maximum 20 overs allowed.",
        )

    # Rule 3: Over numbers must be unique
    for existing in existing_overs:
        if existing.over_number == over.over_number:
            raise HTTPException(
                status_code=400,
                detail="Over number already exists.",
            )

    return create_over(
        db,
        over,
    )