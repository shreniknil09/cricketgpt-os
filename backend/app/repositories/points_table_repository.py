from sqlalchemy.orm import Session

from app.models.match import Match
from app.models.team import Team


def get_tournament_matches(
    db: Session,
    tournament_id: int,
):
    """
    Get all completed matches of a tournament.
    """

    return (
        db.query(Match)
        .filter(
            Match.tournament_id == tournament_id,
            Match.status == "Completed",
        )
        .all()
    )


def get_all_teams(
    db: Session,
):
    """
    Get all teams.
    """

    return db.query(Team).all()