from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.match import Match
from app.models.player_match_stats import PlayerMatchStats
from app.models.bowler_match_stats import BowlerMatchStats


def get_team_batting_stats(
    db: Session,
    team_id: int,
):
    """
    Get aggregate batting statistics for players
    who represented the team.
    """

    return (
        db.query(
            func.coalesce(
                func.sum(PlayerMatchStats.runs),
                0,
            ).label("total_runs"),

            func.coalesce(
                func.sum(PlayerMatchStats.fours),
                0,
            ).label("total_fours"),

            func.coalesce(
                func.sum(PlayerMatchStats.sixes),
                0,
            ).label("total_sixes"),

            func.coalesce(
                func.sum(PlayerMatchStats.balls),
                0,
            ).label("total_balls"),
        )
        .join(
            Match,
            Match.id == PlayerMatchStats.match_id,
        )
        .filter(
            (
                (Match.team1_id == team_id)
                | (Match.team2_id == team_id)
            )
        )
        .first()
    )


def get_team_bowling_stats(
    db: Session,
    team_id: int,
):
    """
    Get aggregate bowling statistics for players
    who represented the team.
    """

    return (
        db.query(
            func.coalesce(
                func.sum(BowlerMatchStats.wickets),
                0,
            ).label("total_wickets"),

            func.coalesce(
                func.sum(BowlerMatchStats.runs_given),
                0,
            ).label("total_runs_given"),

            func.coalesce(
                func.sum(BowlerMatchStats.maidens),
                0,
            ).label("total_maidens"),
        )
        .join(
            Match,
            Match.id == BowlerMatchStats.match_id,
        )
        .filter(
            (
                (Match.team1_id == team_id)
                | (Match.team2_id == team_id)
            )
        )
        .first()
    )


def get_team_match_results(
    db: Session,
    team_id: int,
):
    """
    Get matches involving the team.
    """

    return (
        db.query(Match)
        .filter(
            (
                (Match.team1_id == team_id)
                | (Match.team2_id == team_id)
            )
        )
        .all()
    )