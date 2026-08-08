from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.schemas.match_prediction_v2_schema import (
    MatchPredictionV2Response,
)

from app.services.match_prediction_v2_service import (
    get_match_prediction_v2,
)


router = APIRouter(
    prefix="/match-prediction-v2",
    tags=["Match Prediction V2"],
)


@router.get(
    "/{match_id}",
    response_model=MatchPredictionV2Response,
)
def read_match_prediction_v2(
    match_id: int,
    db: Session = Depends(get_db),
):
    return get_match_prediction_v2(
        db,
        match_id,
    )