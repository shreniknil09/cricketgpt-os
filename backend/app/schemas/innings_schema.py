from pydantic import BaseModel


class InningsCreate(BaseModel):
    match_id: int
    innings_number: int
    batting_team_id: int
    bowling_team_id: int

    current_striker_id: int | None = None
    current_non_striker_id: int | None = None
    current_bowler_id: int | None = None


class InningsResponse(BaseModel):
    id: int

    match_id: int
    innings_number: int

    batting_team_id: int
    bowling_team_id: int

    current_striker_id: int | None
    current_non_striker_id: int | None
    current_bowler_id: int | None

    runs: int
    wickets: int
    overs: int
    balls: int

    status: str

    class Config:
        from_attributes = True