from datetime import date, time

from app.models.match import Match
from app.models.team import Team
from app.models.tournament import Tournament
from app.models.venue import Venue


def seed_matches(db):

    tournament = (
        db.query(Tournament)
        .filter(Tournament.name == "ICC Cricket World Cup")
        .first()
    )

    venue = (
        db.query(Venue)
        .filter(Venue.name == "Narendra Modi Stadium")
        .first()
    )

    india = (
        db.query(Team)
        .filter(Team.short_name == "IND")
        .first()
    )

    australia = (
        db.query(Team)
        .filter(Team.short_name == "AUS")
        .first()
    )

    if not all([tournament, venue, india, australia]):
        print("❌ Required data not found. Run previous seeders first.")
        return

    existing_match = (
        db.query(Match)
        .filter(
            Match.tournament_id == tournament.id,
            Match.team1_id == india.id,
            Match.team2_id == australia.id,
        )
        .first()
    )

    if existing_match:
        print("✓ India vs Australia match already exists")
        return

    match = Match(
        tournament_id=tournament.id,
        venue_id=venue.id,
        team1_id=india.id,
        team2_id=australia.id,
        match_date=date(2026, 8, 15),
        match_time=time(19, 30),
        status="Scheduled",
    )

    db.add(match)
    db.commit()

    print("1 match created successfully.")