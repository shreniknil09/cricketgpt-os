from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.schemas.venue_analysis_schema import (
    VenueAnalysisResponse,
)

from app.services.venue_analysis_service import (
    get_venue_analysis,
)


router = APIRouter(
    prefix="/venue-analysis",
    tags=["Venue Analysis"],
)


@router.get(
    "/{team_id}/{venue_id}",
    response_model=VenueAnalysisResponse,
)
def read_venue_analysis(
    team_id: int,
    venue_id: int,
    db: Session = Depends(get_db),
):
    return get_venue_analysis(
        db,
        team_id,
        venue_id,
    )