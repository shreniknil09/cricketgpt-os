from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.bowling_spell_schema import BowlingSpellResponse
from app.services.bowling_spell_service import get_bowling_spell


router = APIRouter(
    prefix="/bowling-spell",
    tags=["Bowling Spell"],
)


@router.get(
    "/{player_id}",
    response_model=BowlingSpellResponse,
)
def read_bowling_spell(
    player_id: int,
    db: Session = Depends(get_db),
):
    return get_bowling_spell(
        db,
        player_id,
    )