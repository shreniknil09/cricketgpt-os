from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.schemas.team_form_schema import (
    TeamFormResponse,
)

from app.services.team_form_service import (
    get_team_form,
)


router = APIRouter(
    prefix="/team-form",
    tags=["Team Form"],
)


@router.get(
    "/{team_id}",
    response_model=TeamFormResponse,
)
def read_team_form(
    team_id: int,
    db: Session = Depends(get_db),
):
    return get_team_form(
        db,
        team_id,
    )