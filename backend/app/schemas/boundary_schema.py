from pydantic import BaseModel


class BoundaryResponse(BaseModel):
    match_id: int
    innings_id: int

    fours: int
    sixes: int
    total_boundaries: int

    boundary_runs: int
    boundary_percentage: float

    boundary_status: str