from sqlalchemy.orm import Session

from app.models.innings import Innings


def get_all_innings(db: Session):
    return db.query(Innings).all()


def get_innings_by_id(
    db: Session,
    innings_id: int,
):
    return (
        db.query(Innings)
        .filter(Innings.id == innings_id)
        .first()
    )


def get_match_innings(
    db: Session,
    match_id: int,
):
    return (
        db.query(Innings)
        .filter(Innings.match_id == match_id)
        .all()
    )


def create_innings(
    db: Session,
    innings,
):
    new_innings = Innings(
        match_id=innings.match_id,
        innings_number=innings.innings_number,
        batting_team_id=innings.batting_team_id,
        bowling_team_id=innings.bowling_team_id,
    )

    db.add(new_innings)
    db.commit()
    db.refresh(new_innings)

    return new_innings