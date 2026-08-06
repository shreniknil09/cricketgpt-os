from pydantic import BaseModel


class CommentaryResponse(BaseModel):
    over_number: int
    ball_number: int
    commentary: str | None
    runs: int
    extra_type: str |None
    extra_runs: int
    is_wicket: bool
    dismissal_type: str | None

    class Config:
        from_attributes = True