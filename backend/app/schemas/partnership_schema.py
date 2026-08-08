from pydantic import BaseModel


class PartnershipResponse(BaseModel):
    innings_id: int
    striker_id: int
    non_striker_id: int
    runs: int
    balls: int