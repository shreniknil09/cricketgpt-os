from pydantic import BaseModel


class InningsSummary(BaseModel):
    innings_number: int
    batting_team_id: int
    bowling_team_id: int
    runs: int
    wickets: int
    overs: int
    balls: int
    status: str

    class Config:
        from_attributes = True


class MatchSummaryResponse(BaseModel):
    match_id: int
    team1_id: int
    team2_id: int
    venue_id: int
    tournament_id: int
    status: str
    innings: list[InningsSummary]