from pydantic import BaseModel


class TeamFormResponse(BaseModel):
    team_id: int

    matches: int
    wins: int
    losses: int

    win_rate: float
    form_rating: float
    form_status: str