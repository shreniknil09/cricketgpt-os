from pydantic import BaseModel


class VenueCreate(BaseModel):
    name: str
    city: str
    country: str
    capacity: int


class VenueResponse(VenueCreate):
    id: int

    class Config:
        from_attributes = True