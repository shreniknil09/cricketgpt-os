from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.schemas.player_career_schema import (
    PlayerCareerResponse,
)

from app.services.player_career_service import (
    get_player_career,
)

router = APIRouter(
    prefix="/player-career",
    tags=["Player Career"],
)


@router.get(
    "/{player_id}",
    response_model=PlayerCareerResponse,
)
def read_player_career(
    player_id: int,
    db: Session = Depends(get_db),
):
    return get_player_career(
        db,
        player_id,
    )