from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.schemas.match_situation_schema import (
    MatchSituationResponse,
)

from app.services.match_situation_service import (
    get_match_situation,
)


router = APIRouter(
    prefix="/match-situation",
    tags=["Match Situation"],
)


@router.get(
    "/{match_id}",
    response_model=MatchSituationResponse,
)
def read_match_situation(
    match_id: int,
    db: Session = Depends(get_db),
):
    return get_match_situation(
        db,
        match_id,
    )