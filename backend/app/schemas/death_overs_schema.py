from pydantic import BaseModel


class DeathOversResponse(BaseModel):
    match_id: int
    innings_id: int

    runs: int
    wickets: int
    legal_balls: int

    run_rate: float

    boundaries: int
    dot_balls: int
    dot_ball_percentage: float

    status: str