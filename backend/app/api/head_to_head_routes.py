from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.schemas.head_to_head_schema import (
    HeadToHeadResponse,
)

from app.services.head_to_head_service import (
    get_head_to_head,
)


router = APIRouter(
    prefix="/head-to-head",
    tags=["Head-to-Head"],
)


@router.get(
    "/{team1_id}/{team2_id}",
    response_model=HeadToHeadResponse,
)
def read_head_to_head(
    team1_id: int,
    team2_id: int,
    db: Session = Depends(get_db),
):
    return get_head_to_head(
        db,
        team1_id,
        team2_id,
    )