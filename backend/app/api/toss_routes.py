from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.toss import TossCreate, TossResponse
from app.services.toss_service import (
    add_toss,
    get_toss,
    get_tosses,
)

router = APIRouter(
    prefix="/toss",
    tags=["Toss"],
)


@router.get(
    "/",
    response_model=list[TossResponse],
)
def read_tosses(db: Session = Depends(get_db)):
    return get_tosses(db)


@router.get(
    "/{toss_id}",
    response_model=TossResponse,
)
def read_toss(
    toss_id: int,
    db: Session = Depends(get_db),
):
    return get_toss(db, toss_id)


@router.post(
    "/",
    response_model=TossResponse,
)
def create_new_toss(
    toss: TossCreate,
    db: Session = Depends(get_db),
):
    return add_toss(db, toss)