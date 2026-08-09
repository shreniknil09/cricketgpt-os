from pydantic import BaseModel


class MomentumV2Response(BaseModel):
    match_id: int
    innings_id: int

    batting_momentum: float
    bowling_momentum: float

    run_rate_change: float
    boundary_difference: int
    dot_ball_difference: int

    momentum_status: str