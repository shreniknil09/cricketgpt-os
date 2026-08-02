from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.playing_xi import (
    PlayingXICreate,
    PlayingXIResponse,
)
from app.services.playing_xi_service import (
    add_player,
    get_player,
    get_playing_xi,
)

router = APIRouter(
    prefix="/playing-xi",
    tags=["Playing XI"],
)


@router.get("/", response_model=list[PlayingXIResponse])
def get_all(db: Session = Depends(get_db)):
    return get_playing_xi(db)


@router.get("/{playing_xi_id}", response_model=PlayingXIResponse)
def get_one(
    playing_xi_id: int,
    db: Session = Depends(get_db),
):
    try:
        return get_player(db, playing_xi_id)
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


@router.post("/", response_model=PlayingXIResponse)
def create(
    player: PlayingXICreate,
    db: Session = Depends(get_db),
):
    return add_player(db, player)