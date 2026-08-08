from sqlalchemy.orm import Session

from app.models.match import Match


def get_head_to_head_matches(
    db: Session,
    team1_id: int,
    team2_id: int,
):
    """
    Get completed matches played between two teams.
    """

    return (
        db.query(Match)
        .filter(
            Match.status == "Completed",
            (
                (
                    (Match.team1_id == team1_id)
                    & (Match.team2_id == team2_id)
                )
                |
                (
                    (Match.team1_id == team2_id)
                    & (Match.team2_id == team1_id)
                )
            ),
        )
        .order_by(
            Match.match_date.desc(),
            Match.id.desc(),
        )
        .all()
    )