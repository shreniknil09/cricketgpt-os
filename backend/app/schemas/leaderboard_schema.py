from pydantic import BaseModel


class LeaderboardPlayer(BaseModel):
    player_id: int
    value: int

    class Config:
        from_attributes = True


class LeaderboardResponse(BaseModel):
    orange_cap: LeaderboardPlayer
    purple_cap: LeaderboardPlayer
    most_sixes: LeaderboardPlayer
    most_fours: LeaderboardPlayer