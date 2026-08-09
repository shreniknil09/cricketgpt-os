from sqlalchemy.orm import Session

from app.models.match import Match


def get_completed_matches(
    db: Session,
):
    """
    Return completed matches that have a winner.

    These matches can be used for supervised ML training.
    """

    return (
        db.query(Match)
        .filter(
            Match.winner_id.isnot(None),
            Match.status.ilike("Completed"),
        )
        .order_by(
            Match.match_date.asc(),
            Match.id.asc(),
        )
        .all()
    )


def get_match_target(
    match: Match,
):
    """
    Create the supervised-learning target.

    1 = Team 1 won
    0 = Team 2 won
    """

    if match.winner_id == match.team1_id:
        return 1

    if match.winner_id == match.team2_id:
        return 0

    return None


def build_base_match_record(
    match: Match,
):
    """
    Extract reliable base-level information
    directly available from the Match model.
    """

    target = get_match_target(
        match
    )

    if target is None:
        return None

    return {
        "match_id": match.id,

        "team1_id": match.team1_id,
        "team2_id": match.team2_id,

        "venue_id": match.venue_id,

        "toss_winner_id": (
            match.toss_winner_id
            if match.toss_winner_id is not None
            else 0
        ),

        "toss_decision": (
            match.toss_decision
            if match.toss_decision
            else "Unknown"
        ),

        "team1_win": target,
    }


def extract_base_training_records(
    db: Session,
):
    """
    Extract all completed historical matches
    into base training records.
    """

    matches = get_completed_matches(
        db
    )

    records = []

    for match in matches:

        record = build_base_match_record(
            match
        )

        if record is not None:
            records.append(record)

    return records