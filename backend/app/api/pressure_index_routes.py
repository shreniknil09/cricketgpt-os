from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.pressure_index_schema import PressureIndexResponse
from app.services.pressure_index_service import get_pressure_index


router = APIRouter(
    prefix="/pressure-index",
    tags=["Pressure Index"],
)


@router.get(
    "/{match_id}",
    response_model=PressureIndexResponse,
)
def read_pressure_index(
    match_id: int,
    db: Session = Depends(get_db),
):
    return get_pressure_index(
        db,
        match_id,
    )