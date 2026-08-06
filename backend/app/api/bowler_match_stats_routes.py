from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.schemas.bowler_match_stats_schema import (
    BowlerMatchStatsCreate,
    BowlerMatchStatsResponse,
)

from app.services.bowler_match_stats_service import (
    add_bowler_stats,
    get_bowler_stats,
    get_single_bowler_stats,
)

router = APIRouter(
    prefix="/bowler-match-stats",
    tags=["Bowler Match Stats"],
)


@router.get(
    "/",
    response_model=list[BowlerMatchStatsResponse],
)
def read_bowler_stats(
    db: Session = Depends(get_db),
):
    return get_bowler_stats(db)


@router.get(
    "/{stats_id}",
    response_model=BowlerMatchStatsResponse,
)
def read_single_bowler_stats(
    stats_id: int,
    db: Session = Depends(get_db),
):
    return get_single_bowler_stats(
        db,
        stats_id,
    )


@router.post(
    "/",
    response_model=BowlerMatchStatsResponse,
)
def create_bowler_stats_route(
    stats: BowlerMatchStatsCreate,
    db: Session = Depends(get_db),
):
    return add_bowler_stats(
        db,
        stats,
    )