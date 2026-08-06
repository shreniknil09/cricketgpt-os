from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.over_schema import (
    OverCreate,
    OverResponse,
)
from app.services.over_service import (
    add_over,
    get_overs,
    get_single_over,
)

router = APIRouter(
    prefix="/overs",
    tags=["Overs"],
)


@router.get(
    "/",
    response_model=list[OverResponse],
)
def read_overs(
    db: Session = Depends(get_db),
):
    return get_overs(db)


@router.get(
    "/{over_id}",
    response_model=OverResponse,
)
def read_single_over(
    over_id: int,
    db: Session = Depends(get_db),
):
    return get_single_over(
        db,
        over_id,
    )


@router.post(
    "/",
    response_model=OverResponse,
)
def create_new_over(
    over: OverCreate,
    db: Session = Depends(get_db),
):
    return add_over(
        db,
        over,
    )