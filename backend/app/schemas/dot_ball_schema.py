from pydantic import BaseModel


class DotBallResponse(BaseModel):
    match_id: int
    innings_id: int

    dot_balls: int
    legal_balls: int

    dot_ball_percentage: float

    pressure_level: str