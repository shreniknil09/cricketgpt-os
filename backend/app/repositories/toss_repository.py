from sqlalchemy.orm import Session

from app.models.toss import Toss


def get_all_tosses(db: Session):
    return db.query(Toss).all()


def get_toss_by_id(db: Session, toss_id: int):
    return (
        db.query(Toss)
        .filter(Toss.id == toss_id)
        .first()
    )


def get_toss_by_match(db: Session, match_id: int):
    return (
        db.query(Toss)
        .filter(Toss.match_id == match_id)
        .first()
    )


def create_toss(db: Session, toss):

    new_toss = Toss(
        match_id=toss.match_id,
        winning_team_id=toss.winning_team_id,
        decision=toss.decision,
        batting_team_id=toss.batting_team_id,
        bowling_team_id=toss.bowling_team_id,
    )

    db.add(new_toss)
    db.commit()
    db.refresh(new_toss)

    return new_toss