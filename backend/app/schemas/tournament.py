from pydantic import BaseModel


class TournamentCreate(BaseModel):
    name: str
    format: str
    season: str
    country: str


class TournamentResponse(TournamentCreate):
    id: int

    class Config:
        from_attributes = True