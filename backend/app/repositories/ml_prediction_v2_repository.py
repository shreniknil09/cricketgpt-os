from sqlalchemy.orm import Session

from app.models.match import Match


def get_match(
    db: Session,
    match_id: int,
):
    """
    Get a specific match.
    """

    return (
        db.query(Match)
        .filter(
            Match.id == match_id,
        )
        .first()
    )


def get_completed_matches(
    db: Session,
):
    """
    Get historical completed matches
    with known winners.
    """

    return (
        db.query(Match)
        .filter(
            Match.status == "Completed",
            Match.winner_id.isnot(None),
        )
        .order_by(
            Match.match_date.asc(),
            Match.id.asc(),
        )
        .all()
    )