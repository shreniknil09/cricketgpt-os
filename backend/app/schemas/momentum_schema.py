from pydantic import BaseModel


class MomentumResponse(BaseModel):
    match_id: int
    momentum_score: float
    momentum_team_id: int
    momentum: str
    reason: str