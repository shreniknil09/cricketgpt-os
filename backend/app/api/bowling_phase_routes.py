from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.schemas.bowling_phase_schema import (
    BowlingPhaseResponse,
)

from app.services.bowling_phase_service import (
    get_bowling_phase,
)


router = APIRouter(
    prefix="/bowling-phase",
    tags=["Bowling Phase"],
)


@router.get(
    "/{match_id}",
    response_model=BowlingPhaseResponse,
)
def read_bowling_phase(
    match_id: int,
    db: Session = Depends(get_db),
):
    return get_bowling_phase(
        db,
        match_id,
    )