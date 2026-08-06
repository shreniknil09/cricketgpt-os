from pydantic import BaseModel


class BallCreate(BaseModel):
    over_id: int
    ball_number: int
    striker_id: int
    non_striker_id: int
    bowler_id: int
    runs: int = 0
    extra_type: str | None = None
    extra_runs: int = 0
    is_wicket: bool = False
    dismissal_type: str | None = None
    commentary: str | None = None


class BallResponse(BaseModel):
    id: int
    over_id: int
    ball_number: int
    striker_id: int
    non_striker_id: int
    bowler_id: int
    runs: int
    extra_type: str | None
    extra_runs: int
    is_wicket: bool
    dismissal_type: str | None
    commentary: str | None

    class Config:
        from_attributes = True