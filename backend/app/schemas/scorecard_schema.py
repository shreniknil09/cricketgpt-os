from pydantic import BaseModel


class InningsScore(BaseModel):
    runs: int
    wickets: int
    overs: int
    balls: int

    class Config:
        from_attributes = True


class BattingScore(BaseModel):
    player_id: int
    runs: int
    balls: int
    fours: int
    sixes: int
    strike_rate: float
    is_out: bool

    class Config:
        from_attributes = True


class BowlingScore(BaseModel):
    player_id: int
    overs: float
    balls: int
    maidens: int
    runs_given: int
    wickets: int
    economy: float

    class Config:
        from_attributes = True


class ScorecardResponse(BaseModel):
    innings: InningsScore
    batting: list[BattingScore]
    bowling: list[BowlingScore]