from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.dot_ball_schema import DotBallResponse
from app.services.dot_ball_service import get_dot_ball_analysis


router = APIRouter(
    prefix="/dot-balls",
    tags=["Dot Ball Analysis"],
)


@router.get(
    "/{match_id}",
    response_model=DotBallResponse,
)
def read_dot_ball_analysis(
    match_id: int,
    db: Session = Depends(get_db),
):
    return get_dot_ball_analysis(
        db,
        match_id,
    )