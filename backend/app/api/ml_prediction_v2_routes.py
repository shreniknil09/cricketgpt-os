from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.schemas.ml_prediction_v2_schema import (
    MLPredictionV2Response,
)

from app.services.ml_prediction_v2_service import (
    get_ml_prediction_v2,
)


router = APIRouter(
    prefix="/ml-prediction-v2",
    tags=["ML Prediction V2"],
)


@router.get(
    "/{match_id}",
    response_model=MLPredictionV2Response,
)
def read_ml_prediction_v2(
    match_id: int,
    db: Session = Depends(get_db),
):
    return get_ml_prediction_v2(
        db,
        match_id,
    )