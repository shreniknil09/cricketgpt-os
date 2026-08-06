from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.schemas.match_summary_schema import (
    MatchSummaryResponse,
)

from app.services.match_summary_service import (
    get_summary,
)

router = APIRouter(
    prefix="/match-summary",
    tags=["Match Summary"],
)


@router.get(
    "/{match_id}",
    response_model=MatchSummaryResponse,
)
def read_match_summary(
    match_id: int,
    db: Session = Depends(get_db),
):
    return get_summary(
        db,
        match_id,
    )