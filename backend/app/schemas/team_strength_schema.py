from pydantic import BaseModel


class TeamStrengthResponse(BaseModel):
    team_id: int

    batting_strength: float
    bowling_strength: float
    win_strength: float
    overall_strength: float