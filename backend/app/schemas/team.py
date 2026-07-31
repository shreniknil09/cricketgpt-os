from pydantic import BaseModel


class TeamCreate(BaseModel):
    name: str
    short_name: str
    country: str


class TeamResponse(TeamCreate):
    id: int

    class Config:
        from_attributes = True