from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.partnership_v2_schema import PartnershipV2Response
from app.services.partnership_v2_service import get_partnership_analysis


router = APIRouter(
    prefix="/partnership-v2",
    tags=["Partnership v2"],
)


@router.get(
    "/{match_id}",
    response_model=PartnershipV2Response,
)
def read_partnership_analysis(
    match_id: int,
    db: Session = Depends(get_db),
):
    return get_partnership_analysis(
        db,
        match_id,
    )