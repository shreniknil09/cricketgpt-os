from pydantic import BaseModel


class PowerplayResponse(BaseModel):
    match_id: int
    innings_id: int
    runs: int
    wickets: int
    legal_balls: int
    run_rate: float
    boundaries: int
    status: str