from pydantic import BaseModel


class PlayerFormResponse(BaseModel):
    player_id: int

    matches: int

    batting_score: float
    bowling_score: float

    runs: int
    wickets: int

    average_runs: float
    average_wickets: float

    form_rating: float
    form_status: str