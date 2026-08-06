from pydantic import BaseModel


class PlayerCareerResponse(BaseModel):
    player_id: int

    matches: int

    runs: int
    balls: int
    fours: int
    sixes: int
    strike_rate: float

    wickets: int
    overs: float
    economy: float