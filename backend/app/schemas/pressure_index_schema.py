from pydantic import BaseModel


class PressureIndexResponse(BaseModel):
    match_id: int
    innings_id: int

    dot_ball_percentage: float
    required_run_rate: float
    wickets_lost: int

    pressure_score: float
    pressure_status: str