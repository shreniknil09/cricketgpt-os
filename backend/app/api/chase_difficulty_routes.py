from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.chase_difficulty_schema import ChaseDifficultyResponse
from app.services.chase_difficulty_service import get_chase_difficulty


router = APIRouter(
    prefix="/chase-difficulty",
    tags=["Chase Difficulty"],
)


@router.get(
    "/{match_id}",
    response_model=ChaseDifficultyResponse,
)
def read_chase_difficulty(
    match_id: int,
    db: Session = Depends(get_db),
):
    return get_chase_difficulty(
        db,
        match_id,
    )