from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.ball_schema import (
    BallCreate,
    BallResponse,
)
from app.services.ball_service import (
    add_ball,
    get_balls,
    get_single_ball,
)

router = APIRouter(
    prefix="/balls",
    tags=["Balls"],
)


@router.get(
    "/",
    response_model=list[BallResponse],
)
def read_balls(
    db: Session = Depends(get_db),
):
    return get_balls(db)


@router.get(
    "/{ball_id}",
    response_model=BallResponse,
)
def read_single_ball(
    ball_id: int,
    db: Session = Depends(get_db),
):
    return get_single_ball(
        db,
        ball_id,
    )


@router.post(
    "/",
    response_model=BallResponse,
)
def create_new_ball(
    ball: BallCreate,
    db: Session = Depends(get_db),
):
    return add_ball(
        db,
        ball,
    )