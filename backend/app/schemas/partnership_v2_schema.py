from pydantic import BaseModel


class PartnershipV2Response(BaseModel):
    match_id: int
    innings_id: int

    partnership_count: int

    total_partnership_runs: int

    highest_partnership: int
    average_partnership: float

    strongest_partnership: str