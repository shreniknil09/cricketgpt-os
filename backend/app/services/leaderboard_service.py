from sqlalchemy.orm import Session

from app.repositories.leaderboard_repository import (
    get_orange_cap,
    get_purple_cap,
    get_most_sixes,
    get_most_fours,
)


def get_leaderboard(
    db: Session,
):
    """
    Return tournament leaderboard statistics.
    """

    orange = get_orange_cap(db)
    purple = get_purple_cap(db)
    sixes = get_most_sixes(db)
    fours = get_most_fours(db)

    return {
        "orange_cap": {
            "player_id": orange.player_id if orange else 0,
            "value": orange.total_runs if orange else 0,
        },
        "purple_cap": {
            "player_id": purple.player_id if purple else 0,
            "value": purple.total_wickets if purple else 0,
        },
        "most_sixes": {
            "player_id": sixes.player_id if sixes else 0,
            "value": sixes.total_sixes if sixes else 0,
        },
        "most_fours": {
            "player_id": fours.player_id if fours else 0,
            "value": fours.total_fours if fours else 0,
        },
    }