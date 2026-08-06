from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.over import Over
from app.repositories.ball_repository import (
    create_ball,
    count_legal_balls,
    get_all_balls,
    get_ball_by_id,
)
from app.services.match_engine import process_ball


def get_balls(db: Session):
    return get_all_balls(db)


def get_single_ball(
    db: Session,
    ball_id: int,
):
    ball = get_ball_by_id(db, ball_id)

    if ball is None:
        raise HTTPException(
            status_code=404,
            detail="Ball not found.",
        )

    return ball


def add_ball(
    db: Session,
    ball,
):
    # Rule 1: Over must exist
    over = (
        db.query(Over)
        .filter(Over.id == ball.over_id)
        .first()
    )

    if over is None:
        raise HTTPException(
            status_code=404,
            detail="Over not found.",
        )

    # Rule 2: Over not completed
    if over.status == "Completed":
        raise HTTPException(
            status_code=400,
            detail="This over has already been completed.",
        )

    # Rule 3: Maximum 6 legal deliveries
    legal_balls = count_legal_balls(
        db,
        ball.over_id,
    )

    if (
        ball.extra_type not in ["Wide", "No Ball"]
        and legal_balls >= 6
    ):
        raise HTTPException(
            status_code=400,
            detail="This over already has 6 legal deliveries.",
        )

    # Rule 4: Ball number validation
    if ball.ball_number < 1:
        raise HTTPException(
            status_code=400,
            detail="Ball number must start from 1.",
        )

    # Save Ball
    new_ball = create_ball(
        db,
        ball,
    )

    # Process Match Engine
    process_ball(
        db,
        new_ball,
    )

    return new_ball