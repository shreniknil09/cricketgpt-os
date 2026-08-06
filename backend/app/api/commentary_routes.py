from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.schemas.commentary_schema import (
    CommentaryResponse,
)

from app.services.commentary_service import (
    get_commentary,
)

router = APIRouter(
    prefix="/commentary",
    tags=["Commentary"],
)


@router.get(
    "/{match_id}",
    response_model=list[CommentaryResponse],
)
def read_commentary(
    match_id: int,
    db: Session = Depends(get_db),
):
    return get_commentary(
        db,
        match_id,
    )