from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.venue import VenueCreate, VenueResponse
from app.services.venue_service import (
    add_venue,
    get_venue,
    get_venues,
)

router = APIRouter(
    prefix="/venues",
    tags=["Venues"],
)


@router.get("/", response_model=list[VenueResponse])
def get_all(db: Session = Depends(get_db)):
    return get_venues(db)


@router.get("/{venue_id}", response_model=VenueResponse)
def get_one(
    venue_id: int,
    db: Session = Depends(get_db),
):
    try:
        return get_venue(db, venue_id)
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


@router.post("/", response_model=VenueResponse)
def create(
    venue: VenueCreate,
    db: Session = Depends(get_db),
):
    return add_venue(db, venue)