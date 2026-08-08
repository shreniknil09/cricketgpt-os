from sqlalchemy.orm import Session

from app.models.match import Match


RECENT_MATCH_LIMIT = 5


def get_recent_team_matches(
    db: Session,
    team_id: int,
):
    """
    Get the team's most recent completed matches.
    """

    return (
        db.query(Match)
        .filter(
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
        .limit(RECENT_MATCH_LIMIT)
        .all()
    )