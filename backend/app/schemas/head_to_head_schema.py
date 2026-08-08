from pydantic import BaseModel


class HeadToHeadResponse(BaseModel):
    team1_id: int
    team2_id: int

    matches: int

    team1_wins: int
    team2_wins: int

    team1_win_rate: float
    team2_win_rate: float

    dominant_team_id: int | None