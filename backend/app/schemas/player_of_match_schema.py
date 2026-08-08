from pydantic import BaseModel


class PlayerOfMatchResponse(BaseModel):
    match_id: int
    player_id: int
    score: float
