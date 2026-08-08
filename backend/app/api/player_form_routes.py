from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.schemas.player_form_schema import (
    PlayerFormResponse,
)

from app.services.player_form_service import (
    get_player_form,
)


router = APIRouter(
    prefix="/player-form",
    tags=["Player Form"],
)


@router.get(
    "/{player_id}",
    response_model=PlayerFormResponse,
)
def read_player_form(
    player_id: int,
    db: Session = Depends(get_db),
):
    return get_player_form(
        db,
        player_id,
    )