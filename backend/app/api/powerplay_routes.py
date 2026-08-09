from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.powerplay_schema import PowerplayResponse
from app.services.powerplay_service import get_powerplay


router = APIRouter(
    prefix="/powerplay",
    tags=["Powerplay"],
)


@router.get(
    "/{match_id}",
    response_model=PowerplayResponse,
)
def read_powerplay(
    match_id: int,
    db: Session = Depends(get_db),
):
    return get_powerplay(db, match_id)