from sqlalchemy.orm import Session

from app.models.match import Match
from app.models.innings import Innings


def process_result(
    db: Session,
    match_id: int,
):
    """
    Determine and store the result of a completed match.

    The match is completed only when both innings
    have been completed.
    """

    # ---------------------------------
    # Get Match
    # ---------------------------------

    match = (
        db.query(Match)
        .filter(
            Match.id == match_id,
        )
        .first()
    )

    if match is None:
        return

    # ---------------------------------
    # Get Match Innings
    # ---------------------------------

    innings_list = (
        db.query(Innings)
        .filter(
            Innings.match_id == match_id,
        )
        .order_by(
            Innings.innings_number,
        )
        .all()
    )

    # ---------------------------------
    # Match must have two innings
    # ---------------------------------

    if len(innings_list) < 2:
        return

    # ---------------------------------
    # Both innings must be completed
    # ---------------------------------

    if any(
        innings.status != "Completed"
        for innings in innings_list[:2]
    ):
        return

    first_innings = innings_list[0]
    second_innings = innings_list[1]

    # ---------------------------------
    # Determine Winner
    # ---------------------------------

    if first_innings.runs > second_innings.runs:

        match.winner_id = (
            first_innings.batting_team_id
        )

    elif second_innings.runs > first_innings.runs:

        match.winner_id = (
            second_innings.batting_team_id
        )

    else:
        # Match is tied
        match.winner_id = None

    # ---------------------------------
    # Complete Match
    # ---------------------------------

    match.status = "Completed"

    db.commit()
    db.refresh(match)

    return match