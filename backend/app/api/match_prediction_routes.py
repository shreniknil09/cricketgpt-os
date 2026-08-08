from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.schemas.match_prediction_schema import (
    MatchPredictionResponse,
)

from app.services.match_prediction_service import (
    get_match_prediction,
)


router = APIRouter(
    prefix="/match-prediction",
    tags=["Match Prediction"],
)


@router.get(
    "/{match_id}",
    response_model=MatchPredictionResponse,
)
def read_match_prediction(
    match_id: int,
    db: Session = Depends(get_db),
):
    return get_match_prediction(
        db,
        match_id,
    )