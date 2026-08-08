from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.schemas.team_strength_schema import (
    TeamStrengthResponse,
)

from app.services.team_strength_service import (
    get_team_strength,
)


router = APIRouter(
    prefix="/team-strength",
    tags=["Team Strength"],
)


@router.get(
    "/{team_id}",
    response_model=TeamStrengthResponse,
)
def read_team_strength(
    team_id: int,
    db: Session = Depends(get_db),
):
    return get_team_strength(
        db,
        team_id,
    )