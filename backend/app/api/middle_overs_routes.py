from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.middle_overs_schema import MiddleOversResponse
from app.services.middle_overs_service import get_middle_overs


router = APIRouter(
    prefix="/middle-overs",
    tags=["Middle Overs"],
)


@router.get(
    "/{match_id}",
    response_model=MiddleOversResponse,
)
def read_middle_overs(
    match_id: int,
    db: Session = Depends(get_db),
):
    return get_middle_overs(
        db,
        match_id,
    )