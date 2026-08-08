from pydantic import BaseModel


class WinProbabilityResponse(BaseModel):
    match_id: int
    batting_team_id: int
    bowling_team_id: int
    batting_team_probability: float
    bowling_team_probability: float
    runs_required: int
    balls_remaining: int
    wickets_remaining: int