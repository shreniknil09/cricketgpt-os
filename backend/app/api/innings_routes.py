from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.innings_schema import (
    InningsCreate,
    InningsResponse,
)
from app.services.innings_service import (
    add_innings,
    get_innings,
    get_single_innings,
)

router = APIRouter(
    prefix="/innings",
    tags=["Innings"],
)


@router.get(
    "/",
    response_model=list[InningsResponse],
)
def read_innings(
    db: Session = Depends(get_db),
):
    return get_innings(db)


@router.get(
    "/{innings_id}",
    response_model=InningsResponse,
)
def read_single_innings(
    innings_id: int,
    db: Session = Depends(get_db),
):
    return get_single_innings(
        db,
        innings_id,
    )


@router.post(
    "/",
    response_model=InningsResponse,
)
def create_new_innings(
    innings: InningsCreate,
    db: Session = Depends(get_db),
):
    return add_innings(
        db,
        innings,
    )