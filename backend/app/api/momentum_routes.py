from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.schemas.momentum_schema import (
    MomentumResponse,
)

from app.services.momentum_service import (
    get_momentum,
)


router = APIRouter(
    prefix="/momentum",
    tags=["Momentum"],
)


@router.get(
    "/{match_id}",
    response_model=MomentumResponse,
)
def read_momentum(
    match_id: int,
    db: Session = Depends(get_db),
):
    return get_momentum(
        db,
        match_id,
    )