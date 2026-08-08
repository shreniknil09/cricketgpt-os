from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.schemas.partnership_schema import (
    PartnershipResponse,
)

from app.services.partnership_service import (
    get_partnerships,
)


router = APIRouter(
    prefix="/partnerships",
    tags=["Partnerships"],
)


@router.get(
    "/{innings_id}",
    response_model=list[PartnershipResponse],
)
def read_partnerships(
    innings_id: int,
    db: Session = Depends(get_db),
):
    return get_partnerships(
        db,
        innings_id,
    )