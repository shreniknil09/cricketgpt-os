from pydantic import BaseModel


class TeamStatsResponse(BaseModel):
    team_id: int

    matches: int

    wins: int

    losses: int

    win_percentage: float

    highest_score: int

    lowest_score: int