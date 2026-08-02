from sqlalchemy.orm import Session

from app.repositories.match_repository import (
    create_match,
    get_all_matches,
    get_match_by_id,
)


def get_matches(db: Session):
    return get_all_matches(db)


def get_match(db: Session, match_id: int):
    match = get_match_by_id(db, match_id)

    if match is None:
        raise Exception("Match not found")

    return match


def add_match(db: Session, match):
    return create_match(db, match)