from pydantic import BaseModel


class PlayerCreate(BaseModel):
    name: str
    batting_style: str
    bowling_style: str
    role: str
    team_id: int


class PlayerResponse(PlayerCreate):
    id: int

    class Config:
        from_attributes = True