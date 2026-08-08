from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.schemas.fall_of_wickets_schema import (
    FallOfWicketResponse,
)

from app.services.fall_of_wickets_service import (
    get_fall_of_wickets,
)


router = APIRouter(
    prefix="/fall-of-wickets",
    tags=["Fall of Wickets"],
)


@router.get(
    "/{innings_id}",
    response_model=list[FallOfWicketResponse],
)
def read_fall_of_wickets(
    innings_id: int,
    db: Session = Depends(get_db),
):
    return get_fall_of_wickets(
        db,
        innings_id,
    )