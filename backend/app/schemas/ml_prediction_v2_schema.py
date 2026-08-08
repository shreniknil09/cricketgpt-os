from pydantic import BaseModel


class MLPredictionV2Response(BaseModel):
    match_id: int

    team1_id: int
    team2_id: int

    team1_probability: float
    team2_probability: float

    predicted_winner_id: int

    model: str