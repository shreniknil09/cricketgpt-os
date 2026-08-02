from datetime import date, time

from pydantic import BaseModel


class MatchCreate(BaseModel):
    tournament_id: int
    venue_id: int
    team1_id: int
    team2_id: int
    match_date: date
    match_time: time


class MatchResponse(MatchCreate):
    id: int
    status: str
    toss_winner_id: int | None = None
    toss_decision: str | None = None
    winner_id: int | None = None

    class Config:
        from_attributes = True