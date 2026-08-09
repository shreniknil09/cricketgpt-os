from pydantic import BaseModel


class BowlingSpellResponse(BaseModel):
    player_id: int

    matches: int

    total_overs: float
    total_runs_given: int
    total_wickets: int

    average_economy: float
    average_wickets: float

    spell_rating: float
    spell_status: str