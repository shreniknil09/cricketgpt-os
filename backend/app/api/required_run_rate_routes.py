from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.required_run_rate_schema import RequiredRunRateResponse
from app.services.required_run_rate_service import get_required_run_rate


router = APIRouter(
    prefix="/required-run-rate",
    tags=["Required Run Rate"],
)


@router.get(
    "/{match_id}",
    response_model=RequiredRunRateResponse,
)
def read_required_run_rate(
    match_id: int,
    db: Session = Depends(get_db),
):
    return get_required_run_rate(
        db,
        match_id,
    )