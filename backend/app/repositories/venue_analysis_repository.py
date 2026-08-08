from sqlalchemy.orm import Session

from app.models.match import Match


def get_venue_team_matches(
    db: Session,
    team_id: int,
    venue_id: int,
):
    """
    Get completed matches played by a team
    at a specific venue.
    """

    return (
        db.query(Match)
        .filter(
            Match.venue_id == venue_id,
            (
                (Match.team1_id == team_id)
                | (Match.team2_id == team_id)
            ),
            Match.status == "Completed",
        )
        .order_by(
            Match.match_date.desc(),
            Match.id.desc(),
        )
        .all()
    )