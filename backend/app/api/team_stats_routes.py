from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.schemas.team_stats_schema import (
    TeamStatsResponse,
)

from app.services.team_stats_service import (
    get_team_statistics,
)

router = APIRouter(
    prefix="/team-stats",
    tags=["Team Statistics"],
)


@router.get(
    "/{team_id}",
    response_model=TeamStatsResponse,
)
def read_team_statistics(
    team_id: int,
    db: Session = Depends(get_db),
):
    return get_team_statistics(
        db,
        team_id,
    )