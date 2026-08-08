from pydantic import BaseModel


class MatchPredictionV2Response(BaseModel):
    match_id: int

    team1_id: int
    team2_id: int

    team1_score: float
    team2_score: float

    team1_probability: float
    team2_probability: float

    predicted_winner_id: int