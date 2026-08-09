from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.momentum_v2_schema import MomentumV2Response
from app.services.momentum_v2_service import get_momentum_v2


router = APIRouter(
    prefix="/momentum-v2",
    tags=["Momentum v2"],
)


@router.get(
    "/{match_id}",
    response_model=MomentumV2Response,
)
def read_momentum_v2(
    match_id: int,
    db: Session = Depends(get_db),
):
    return get_momentum_v2(
        db,
        match_id,
    )