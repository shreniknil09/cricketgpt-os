from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.schemas.player_impact_schema import (
    PlayerImpactResponse,
)

from app.services.player_impact_service import (
    get_player_impact,
)


router = APIRouter(
    prefix="/player-impact",
    tags=["Player Impact"],
)


@router.get(
    "/{match_id}",
    response_model=list[PlayerImpactResponse],
)
def read_player_impact(
    match_id: int,
    db: Session = Depends(get_db),
):
    return get_player_impact(
        db,
        match_id,
    )