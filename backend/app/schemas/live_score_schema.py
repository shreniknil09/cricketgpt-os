from pydantic import BaseModel


class LiveScoreResponse(BaseModel):
    match_id: int
    innings_number: int

    batting_team_id: int
    bowling_team_id: int

    runs: int
    wickets: int
    overs: int
    balls: int

    current_striker_id: int | None
    current_non_striker_id: int | None
    current_bowler_id: int | None

    status: str

    class Config:
        from_attributes = True