from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.schemas.run_rate_schema import (
    RunRateResponse,
)

from app.services.run_rate_service import (
    get_run_rate,
)


router = APIRouter(
    prefix="/run-rate",
    tags=["Run Rate"],
)


@router.get(
    "/{match_id}",
    response_model=RunRateResponse,
)
def read_run_rate(
    match_id: int,
    db: Session = Depends(get_db),
):
    return get_run_rate(
        db,
        match_id,
    )