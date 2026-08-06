from sqlalchemy.orm import Session

from app.models.ball import Ball


def get_all_balls(db: Session):
    return db.query(Ball).all()


def get_ball_by_id(
    db: Session,
    ball_id: int,
):
    return (
        db.query(Ball)
        .filter(Ball.id == ball_id)
        .first()
    )


def get_over_balls(
    db: Session,
    over_id: int,
):
    return (
        db.query(Ball)
        .filter(Ball.over_id == over_id)
        .order_by(Ball.ball_number)
        .all()
    )


def count_legal_balls(
    db: Session,
    over_id: int,
):
    return (
        db.query(Ball)
        .filter(
            Ball.over_id == over_id,
            Ball.extra_type.notin_(["Wide", "No Ball"]),
        )
        .count()
    )


def create_ball(
    db: Session,
    ball,
):
    new_ball = Ball(
        over_id=ball.over_id,
        ball_number=ball.ball_number,
        striker_id=ball.striker_id,
        non_striker_id=ball.non_striker_id,
        bowler_id=ball.bowler_id,
        runs=ball.runs,
        extra_type=ball.extra_type,
        extra_runs=ball.extra_runs,
        is_wicket=ball.is_wicket,
        dismissal_type=ball.dismissal_type,
        commentary=ball.commentary,
    )

    db.add(new_ball)
    db.commit()
    db.refresh(new_ball)

    return new_ball