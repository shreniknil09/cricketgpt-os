from pydantic import BaseModel


class PlayingXICreate(BaseModel):
    match_id: int
    team_id: int
    player_id: int
    batting_position: int
    is_captain: bool = False
    is_wicketkeeper: bool = False


class PlayingXIResponse(PlayingXICreate):
    id: int

    class Config:
        from_attributes = True