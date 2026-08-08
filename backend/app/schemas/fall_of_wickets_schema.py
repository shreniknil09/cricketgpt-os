from pydantic import BaseModel


class FallOfWicketResponse(BaseModel):
    innings_id: int
    wicket_number: int
    player_id: int
    score: int
    over: float