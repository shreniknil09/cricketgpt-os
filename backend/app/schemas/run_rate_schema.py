from pydantic import BaseModel


class RunRateResponse(BaseModel):
    match_id: int
    innings_id: int

    total_runs: int
    legal_balls: int
    current_overs: float

    current_run_rate: float
    recent_run_rate: float

    run_rate_change: float
    trend: str