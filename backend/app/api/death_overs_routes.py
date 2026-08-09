from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.death_overs_schema import DeathOversResponse
from app.services.death_overs_service import get_death_overs


router = APIRouter(
    prefix="/death-overs",
    tags=["Death Overs"],
)


@router.get(
    "/{match_id}",
    response_model=DeathOversResponse,
)
def read_death_overs(
    match_id: int,
    db: Session = Depends(get_db),
):
    return get_death_overs(
        db,
        match_id,
    )