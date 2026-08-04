from app.models.tournament import Tournament


def seed_tournaments(db):

    tournaments = [
        {
            "name": "ICC Cricket World Cup",
            "format": "ODI",
            "season": "2023",
            "country": "India",
        },
        {
            "name": "ICC Champions Trophy",
            "format": "ODI",
            "season": "2025",
            "country": "Pakistan",
        },
        {
            "name": "Indian Premier League",
            "format": "T20",
            "season": "2025",
            "country": "India",
        },
    ]

    created = 0

    for tournament in tournaments:

        existing = (
            db.query(Tournament)
            .filter(Tournament.name == tournament["name"])
            .first()
        )

        if existing:
            print(f"✓ {tournament['name']} already exists")
            continue

        db.add(Tournament(**tournament))
        created += 1

    db.commit()

    print(f"\n{created} tournament(s) created successfully.")