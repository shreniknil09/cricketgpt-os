from pydantic import BaseModel


class VenueAnalysisResponse(BaseModel):
    team_id: int
    venue_id: int

    matches: int
    wins: int
    losses: int

    win_rate: float
    venue_rating: float
    venue_status: str