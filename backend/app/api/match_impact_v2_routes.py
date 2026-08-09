from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.match_impact_v2_schema import MatchImpactV2Response
from app.services.match_impact_v2_service import get_match_impact_v2


router = APIRouter(
    prefix="/match-impact-v2",
    tags=["Match Impact v2"],
)


@router.get(
    "/{match_id}",
    response_model=MatchImpactV2Response,
)
def read_match_impact_v2(
    match_id: int,
    db: Session = Depends(get_db),
):
    return get_match_impact_v2(
        db,
        match_id,
    )