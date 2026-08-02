from app.models.team import Team


def seed_teams(db):
    teams = [
        {
            "name": "India",
            "short_name": "IND",
            "country": "India",
        },
        {
            "name": "Australia",
            "short_name": "AUS",
            "country": "Australia",
        },
    ]

    created = 0

    for team in teams:

        existing_team = (
            db.query(Team)
            .filter(Team.name == team["name"])
            .first()
        )

        if existing_team:
            print(f"✓ {team['name']} already exists")
            continue

        db.add(Team(**team))
        created += 1

    db.commit()

    print(f"\n{created} team(s) created successfully.")