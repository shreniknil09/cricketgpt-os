from pydantic import BaseModel


class ChaseDifficultyResponse(BaseModel):
    match_id: int
    innings_id: int

    runs_remaining: int
    balls_remaining: int

    required_run_rate: float
    wickets_lost: int

    difficulty_score: float
    difficulty_status: str