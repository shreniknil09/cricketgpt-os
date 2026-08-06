from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.schemas.scorecard_schema import (
    ScorecardResponse,
)

from app.services.scorecard_service import (
    get_match_scorecard,
)

router = APIRouter(
    prefix="/scorecard",
    tags=["Scorecard"],
)


@router.get(
    "/{match_id}",
    response_model=ScorecardResponse,
)
def read_scorecard(
    match_id: int,
    db: Session = Depends(get_db),
):
    return get_match_scorecard(
        db,
        match_id,
    )