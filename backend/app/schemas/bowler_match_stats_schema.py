from pydantic import BaseModel


class BowlerMatchStatsCreate(BaseModel):
    match_id: int
    player_id: int


class BowlerMatchStatsResponse(BaseModel):
    id: int
    match_id: int
    player_id: int
    overs: float
    balls: int
    maidens: int
    runs_given: int
    wickets: int
    economy: float

    class Config:
        from_attributes = True