from pydantic import BaseModel


class BattingPhaseResponse(BaseModel):
    match_id: int
    innings_id: int

    powerplay_runs: int
    powerplay_balls: int
    powerplay_run_rate: float

    middle_overs_runs: int
    middle_overs_balls: int
    middle_overs_run_rate: float

    death_overs_runs: int
    death_overs_balls: int
    death_overs_run_rate: float

    best_phase: str