from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.tournament import (
    TournamentCreate,
    TournamentResponse,
)
from app.services.tournament_service import (
    add_tournament,
    get_tournament,
    get_tournaments,
)

router = APIRouter(
    prefix="/tournaments",
    tags=["Tournaments"],
)


@router.get("/", response_model=list[TournamentResponse])
def get_all(db: Session = Depends(get_db)):
    return get_tournaments(db)


@router.get("/{tournament_id}", response_model=TournamentResponse)
def get_one(
    tournament_id: int,
    db: Session = Depends(get_db),
):
    try:
        return get_tournament(db, tournament_id)
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


@router.post("/", response_model=TournamentResponse)
def create(
    tournament: TournamentCreate,
    db: Session = Depends(get_db),
):
    return add_tournament(db, tournament)