from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.team import TeamCreate, TeamResponse
from app.services.team_service import (
    create_team,
    delete_team,
    get_all_teams,
    get_team_by_id,
    update_team,
)

router = APIRouter(
    prefix="/teams",
    tags=["Teams"]
)


@router.get("/", response_model=list[TeamResponse])
def read_teams(db: Session = Depends(get_db)):
    return get_all_teams(db)


@router.get("/{team_id}", response_model=TeamResponse)
def read_team(team_id: int, db: Session = Depends(get_db)):
    team = get_team_by_id(db, team_id)

    if team is None:
        raise HTTPException(status_code=404, detail="Team not found")

    return team


@router.post("/", response_model=TeamResponse)
def add_team(team: TeamCreate, db: Session = Depends(get_db)):
    return create_team(db, team)


@router.put("/{team_id}", response_model=TeamResponse)
def edit_team(
    team_id: int,
    team: TeamCreate,
    db: Session = Depends(get_db),
):
    updated = update_team(db, team_id, team)

    if updated is None:
        raise HTTPException(status_code=404, detail="Team not found")

    return updated


@router.delete("/{team_id}")
def remove_team(
    team_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_team(db, team_id)

    if deleted is None:
        raise HTTPException(status_code=404, detail="Team not found")

    return {
        "message": "Team deleted successfully"
    }