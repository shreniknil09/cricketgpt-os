from sqlalchemy.orm import Session

from app.models.venue import Venue


def get_all_venues(db: Session):
    return db.query(Venue).all()


def get_venue_by_id(db: Session, venue_id: int):
    return db.query(Venue).filter(Venue.id == venue_id).first()


def create_venue(db: Session, venue):
    new_venue = Venue(
        name=venue.name,
        city=venue.city,
        country=venue.country,
        capacity=venue.capacity,
    )

    db.add(new_venue)
    db.commit()
    db.refresh(new_venue)

    return new_venue