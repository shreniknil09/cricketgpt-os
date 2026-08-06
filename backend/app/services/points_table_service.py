from sqlalchemy.orm import Session

from app.repositories.points_table_repository import (
    get_all_teams,
    get_tournament_matches,
)


def get_points_table(
    db: Session,
    tournament_id: int,
):
    """
    Calculate the points table for a tournament.
    """

    teams = get_all_teams(db)

    matches = get_tournament_matches(
        db,
        tournament_id,
    )

    table = []

    for team in teams:

        played = 0
        won = 0
        lost = 0

        for match in matches:

            if (
                team.id == match.team1_id
                or team.id == match.team2_id
            ):

                played += 1

                if (
                    hasattr(match, "winner_team_id")
                    and match.winner_team_id == team.id
                ):
                    won += 1
                else:
                    lost += 1

        table.append(
            {
                "team_id": team.id,
                "played": played,
                "won": won,
                "lost": lost,
                "points": won * 2,
                "net_run_rate": 0.0,
            }
        )

    table.sort(
        key=lambda x: x["points"],
        reverse=True,
    )

    return {
        "teams": table,
    }