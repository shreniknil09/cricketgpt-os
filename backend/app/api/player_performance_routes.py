from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.schemas.player_performance_schema import (
    PlayerPerformanceResponse,
)

from app.services.player_performance_service import (
    get_player_performance,
)


router = APIRouter(
    prefix="/player-performance",
    tags=["Player Performance"],
)


@router.get(
    "/{player_id}",
    response_model=PlayerPerformanceResponse,
)
def read_player_performance(
    player_id: int,
    db: Session = Depends(get_db),
):
    return get_player_performance(
        db,
        player_id,
    )