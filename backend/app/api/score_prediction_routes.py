from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.schemas.score_prediction_schema import (
    ScorePredictionResponse,
)

from app.services.score_prediction_service import (
    get_score_prediction,
)


router = APIRouter(
    prefix="/score-prediction",
    tags=["Score Prediction"],
)


@router.get(
    "/{match_id}",
    response_model=ScorePredictionResponse,
)
def read_score_prediction(
    match_id: int,
    db: Session = Depends(get_db),
):
    return get_score_prediction(
        db,
        match_id,
    )