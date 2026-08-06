from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.schemas.points_table_schema import (
    PointsTableResponse,
)

from app.services.points_table_service import (
    get_points_table,
)

router = APIRouter(
    prefix="/points-table",
    tags=["Points Table"],
)


@router.get(
    "/{tournament_id}",
    response_model=PointsTableResponse,
)
def read_points_table(
    tournament_id: int,
    db: Session = Depends(get_db),
):
    return get_points_table(
        db,
        tournament_id,
    )