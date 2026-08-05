from pydantic import BaseModel


class InningsCreate(BaseModel):
    match_id: int
    innings_number: int
    batting_team_id: int
    bowling_team_id: int


class InningsResponse(BaseModel):
    id: int
    match_id: int
    innings_number: int
    batting_team_id: int
    bowling_team_id: int
    runs: int
    wickets: int
    overs: int
    balls: int
    status: str

    class Config:
        from_attributes = True