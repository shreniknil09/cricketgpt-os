from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.schemas.batting_phase_schema import (
    BattingPhaseResponse,
)

from app.services.batting_phase_service import (
    get_batting_phase,
)


router = APIRouter(
    prefix="/batting-phase",
    tags=["Batting Phase"],
)


@router.get(
    "/{match_id}",
    response_model=BattingPhaseResponse,
)
def read_batting_phase(
    match_id: int,
    db: Session = Depends(get_db),
):
    return get_batting_phase(
        db,
        match_id,
    )