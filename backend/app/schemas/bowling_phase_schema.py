from pydantic import BaseModel


class BowlingPhaseResponse(BaseModel):
    match_id: int
    innings_id: int

    powerplay_runs_given: int
    powerplay_wickets: int
    powerplay_economy: float

    middle_overs_runs_given: int
    middle_overs_wickets: int
    middle_overs_economy: float

    death_overs_runs_given: int
    death_overs_wickets: int
    death_overs_economy: float

    best_phase: str