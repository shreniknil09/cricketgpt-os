from pydantic import BaseModel


class MatchImpactV2Response(BaseModel):
    match_id: int

    team1_id: int
    team2_id: int

    team1_impact: float
    team2_impact: float

    impact_difference: float

    dominant_team_id: int | None

    impact_status: str