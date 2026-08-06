from pydantic import BaseModel


class OverCreate(BaseModel):
    innings_id: int
    over_number: int
    bowler_id: int


class OverResponse(BaseModel):
    id: int
    innings_id: int
    over_number: int
    bowler_id: int
    runs: int
    wickets: int
    status: str

    class Config:
        from_attributes = True