from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.boundary_schema import BoundaryResponse
from app.services.boundary_service import get_boundary_analysis


router = APIRouter(
    prefix="/boundary",
    tags=["Boundary Analysis"],
)


@router.get(
    "/{match_id}",
    response_model=BoundaryResponse,
)
def read_boundary_analysis(
    match_id: int,
    db: Session = Depends(get_db),
):
    return get_boundary_analysis(
        db,
        match_id,
    )