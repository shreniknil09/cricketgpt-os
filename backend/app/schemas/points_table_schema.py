from pydantic import BaseModel


class TeamPoints(BaseModel):
    team_id: int
    played: int
    won: int
    lost: int
    points: int
    net_run_rate: float


class PointsTableResponse(BaseModel):
    teams: list[TeamPoints]