from sqlalchemy.orm import Session

from app.models.match import Match


def get_match(
    db: Session,
    match_id: int,
):
    """
    Get match information.
    """

    return (
        db.query(Match)
        .filter(
            Match.id == match_id,
        )
        .first()
    )