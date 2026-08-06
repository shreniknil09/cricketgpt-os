from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.schemas.leaderboard_schema import (
    LeaderboardResponse,
)

from app.services.leaderboard_service import (
    get_leaderboard,
)

router = APIRouter(
    prefix="/leaderboard",
    tags=["Leaderboard"],
)


@router.get(
    "/",
    response_model=LeaderboardResponse,
)
def read_leaderboard(
    db: Session = Depends(get_db),
):
    return get_leaderboard(
        db,
    )