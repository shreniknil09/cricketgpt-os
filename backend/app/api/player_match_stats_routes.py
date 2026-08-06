from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.schemas.player_match_stats_schema import (
    PlayerMatchStatsCreate,
    PlayerMatchStatsResponse,
)

from app.services.player_match_stats_service import (
    add_player_stats,
    get_player_stats,
    get_single_player_stats,
)

router = APIRouter(
    prefix="/player-match-stats",
    tags=["Player Match Stats"],
)


@router.get(
    "/",
    response_model=list[PlayerMatchStatsResponse],
)
def read_player_stats(
    db: Session = Depends(get_db),
):
    return get_player_stats(db)


@router.get(
    "/{stats_id}",
    response_model=PlayerMatchStatsResponse,
)
def read_single_player_stats(
    stats_id: int,
    db: Session = Depends(get_db),
):
    return get_single_player_stats(
        db,
        stats_id,
    )


@router.post(
    "/",
    response_model=PlayerMatchStatsResponse,
)
def create_player_stats_route(
    stats: PlayerMatchStatsCreate,
    db: Session = Depends(get_db),
):
    return add_player_stats(
        db,
        stats,
    )