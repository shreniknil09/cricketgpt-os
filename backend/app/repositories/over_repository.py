from sqlalchemy.orm import Session

from app.models.over import Over


def get_all_overs(db: Session):
    return db.query(Over).all()


def get_over_by_id(
    db: Session,
    over_id: int,
):
    return (
        db.query(Over)
        .filter(Over.id == over_id)
        .first()
    )


def get_innings_overs(
    db: Session,
    innings_id: int,
):
    return (
        db.query(Over)
        .filter(Over.innings_id == innings_id)
        .all()
    )


def create_over(
    db: Session,
    over,
):
    new_over = Over(
        innings_id=over.innings_id,
        over_number=over.over_number,
        bowler_id=over.bowler_id,
    )

    db.add(new_over)
    db.commit()
    db.refresh(new_over)

    return new_over