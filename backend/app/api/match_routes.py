from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.match import MatchCreate, MatchResponse
from app.services.match_service import (
    add_match,
    get_match,
    get_matches,
)

router = APIRouter(
    prefix="/matches",
    tags=["Matches"],
)


@router.get("/", response_model=list[MatchResponse])
def get_all(db: Session = Depends(get_db)):
    return get_matches(db)


@router.get("/{match_id}", response_model=MatchResponse)
def get_one(
    match_id: int,
    db: Session = Depends(get_db),
):
    try:
        return get_match(db, match_id)
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


@router.post("/", response_model=MatchResponse)
def create(
    match: MatchCreate,
    db: Session = Depends(get_db),
):
    return add_match(db, match)