from sqlalchemy.orm import Session

from app.repositories.tournament_repository import (
    create_tournament,
    get_all_tournaments,
    get_tournament_by_id,
)


def get_tournaments(db: Session):
    return get_all_tournaments(db)


def get_tournament(db: Session, tournament_id: int):
    tournament = get_tournament_by_id(db, tournament_id)

    if tournament is None:
        raise Exception("Tournament not found")

    return tournament


def add_tournament(db: Session, tournament):
    return create_tournament(db, tournament)