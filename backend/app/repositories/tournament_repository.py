from sqlalchemy.orm import Session

from app.models.tournament import Tournament


def get_all_tournaments(db: Session):
    return db.query(Tournament).all()


def get_tournament_by_id(db: Session, tournament_id: int):
    return (
        db.query(Tournament)
        .filter(Tournament.id == tournament_id)
        .first()
    )


def create_tournament(db: Session, tournament):
    new_tournament = Tournament(
        name=tournament.name,
        format=tournament.format,
        season=tournament.season,
        country=tournament.country,
    )

    db.add(new_tournament)
    db.commit()
    db.refresh(new_tournament)

    return new_tournament