from pydantic import BaseModel


class TossBase(BaseModel):
    match_id: int
    winning_team_id: int
    decision: str
    batting_team_id: int
    bowling_team_id: int


class TossCreate(TossBase):
    pass


class TossResponse(TossBase):
    id: int

    model_config = {
        "from_attributes": True
    }