from pydantic import BaseModel


class PlayerMatchStatsCreate(BaseModel):
    match_id: int
    player_id: int


class PlayerMatchStatsResponse(BaseModel):
    id: int
    match_id: int
    player_id: int
    runs: int
    balls: int
    fours: int
    sixes: int
    strike_rate: float
    is_out: bool
    dismissal_type: str | None

    class Config:
        from_attributes = True