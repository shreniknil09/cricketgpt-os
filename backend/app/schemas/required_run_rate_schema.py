from pydantic import BaseModel


class RequiredRunRateResponse(BaseModel):
    match_id: int
    innings_id: int

    target: int
    current_score: int

    runs_remaining: int
    balls_remaining: int

    required_run_rate: float

    chase_status: str