from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.schemas.win_probability_schema import (
    WinProbabilityResponse,
)

from app.services.win_probability_service import (
    get_win_probability,
)


router = APIRouter(
    prefix="/win-probability",
    tags=["Win Probability"],
)


@router.get(
    "/{match_id}",
    response_model=WinProbabilityResponse,
)
def read_win_probability(
    match_id: int,
    db: Session = Depends(get_db),
):
    return get_win_probability(
        db,
        match_id,
    )