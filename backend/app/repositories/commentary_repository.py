from sqlalchemy.orm import Session

from app.models.ball import Ball
from app.models.over import Over
from app.models.innings import Innings


def get_match_commentary(
    db: Session,
    match_id: int,
):
    return (
        db.query(
            Ball,
            Over,
        )
        .join(
            Over,
            Ball.over_id == Over.id,
        )
        .join(
            Innings,
            Over.innings_id == Innings.id,
        )
        .filter(
            Innings.match_id == match_id,
        )
        .order_by(
            Over.over_number,
            Ball.ball_number,
        )
        .all()
    )