from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.player import PlayerCreate, PlayerResponse
from app.services.player_service import (
    create_player,
    get_all_players,
)

router = APIRouter(
    prefix="/players",
    tags=["Players"]
)


@router.get("/", response_model=list[PlayerResponse])
def read_players(db: Session = Depends(get_db)):
    return get_all_players(db)


@router.post("/", response_model=PlayerResponse)
def add_player(
    player: PlayerCreate,
    db: Session = Depends(get_db),
):
    return create_player(db, player)