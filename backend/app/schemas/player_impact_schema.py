from pydantic import BaseModel


class PlayerImpactResponse(BaseModel):
    match_id: int
    player_id: int
    batting_score: float
    bowling_score: float
    total_impact: float