from pydantic import BaseModel


class PlayerPerformanceResponse(BaseModel):
    player_id: int

    matches: int

    expected_runs: int
    expected_wickets: int

    average_runs: float
    average_wickets: float

    performance_rating: float
    performance_status: str