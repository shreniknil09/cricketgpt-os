from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.models.innings import Innings
from app.models.match import Match


def get_team_matches(
    db: Session,
    team_id: int,
):
    """
    Get all matches played by the team.
    """

    return (
        db.query(Match)
        .filter(
            or_(
                Match.team1_id == team_id,
                Match.team2_id == team_id,
            )
        )
        .all()
    )


def get_team_wins(
    db: Session,
    team_id: int,
):
    """
    Get total wins of the team.
    """

    return (
        db.query(Match)
        .filter(
            Match.winner_team_id == team_id,
        )
        .count()
    )


def get_highest_score(
    db: Session,
    team_id: int,
):
    """
    Get highest innings score of the team.
    """

    return (
        db.query(func.max(Innings.runs))
        .filter(
            Innings.batting_team_id == team_id,
        )
        .scalar()
    )


def get_lowest_score(
    db: Session,
    team_id: int,
):
    """
    Get lowest innings score of the team.
    """

    return (
        db.query(func.min(Innings.runs))
        .filter(
            Innings.batting_team_id == team_id,
        )
        .scalar()
    )