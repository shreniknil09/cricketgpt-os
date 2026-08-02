from sqlalchemy.orm import Session

from app.models.match import Match


def get_all_matches(db: Session):
    return db.query(Match).all()


def get_match_by_id(db: Session, match_id: int):
    return (
        db.query(Match)
        .filter(Match.id == match_id)
        .first()
    )


def create_match(db: Session, match):
    new_match = Match(
        tournament_id=match.tournament_id,
        venue_id=match.venue_id,
        team1_id=match.team1_id,
        team2_id=match.team2_id,
        match_date=match.match_date,
        match_time=match.match_time,
    )

    db.add(new_match)
    db.commit()
    db.refresh(new_match)

    return new_match