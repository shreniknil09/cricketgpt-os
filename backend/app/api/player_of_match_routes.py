from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.schemas.player_of_match_schema import (
    PlayerOfMatchResponse,
)

from app.services.player_of_match_service import (
    get_player_of_match,
)


router = APIRouter(
    prefix="/player-of-match",
    tags=["Player of the Match"],
)


@router.get(
    "/{match_id}",
    response_model=PlayerOfMatchResponse,
)
def read_player_of_match(
    match_id: int,
    db: Session = Depends(get_db),
):
    return get_player_of_match(
        db,
        match_id,
    )