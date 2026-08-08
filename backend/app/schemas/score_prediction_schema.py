from pydantic import BaseModel


class ScorePredictionResponse(BaseModel):
    match_id: int

    innings_id: int

    current_score: int
    current_wickets: int

    legal_balls: int
    current_overs: float

    current_run_rate: float

    predicted_score: int

    lower_prediction: int
    upper_prediction: int