from pydantic import BaseModel


class MatchSituationResponse(BaseModel):
    match_id: int

    batting_team_id: int
    bowling_team_id: int

    runs: int
    wickets: int

    overs: int
    balls: int

    current_run_rate: float

    runs_required: int
    balls_remaining: int
    required_run_rate: float

    wickets_remaining: int

    pressure_level: str
    situation: str