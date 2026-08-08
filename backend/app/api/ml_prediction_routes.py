from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.schemas.ml_prediction_schema import (
    MLPredictionResponse,
)

from app.services.ml_prediction_service import (
    get_ml_prediction,
)


router = APIRouter(
    prefix="/ml-prediction",
    tags=["ML Prediction"],
)


@router.get(
    "/{match_id}",
    response_model=MLPredictionResponse,
)
def read_ml_prediction(
    match_id: int,
    db: Session = Depends(get_db),
):
    return get_ml_prediction(
        db,
        match_id,
    )