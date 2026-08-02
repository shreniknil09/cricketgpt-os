from sqlalchemy.orm import Session

from app.repositories.venue_repository import (
    create_venue,
    get_all_venues,
    get_venue_by_id,
)


def get_venues(db: Session):
    return get_all_venues(db)


def get_venue(db: Session, venue_id: int):
    venue = get_venue_by_id(db, venue_id)

    if venue is None:
        raise Exception("Venue not found")

    return venue


def add_venue(db: Session, venue):
    return create_venue(db, venue)