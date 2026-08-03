from app.models.venue import Venue


def seed_venues(db):

    venues = [
        {
            "name": "Narendra Modi Stadium",
            "city": "Ahmedabad",
            "country": "India",
            "capacity": 132000,
        },
        {
            "name": "M. Chinnaswamy Stadium",
            "city": "Bengaluru",
            "country": "India",
            "capacity": 40000,
        },
        {
            "name": "Melbourne Cricket Ground",
            "city": "Melbourne",
            "country": "Australia",
            "capacity": 100024,
        },
    ]

    created = 0

    for venue in venues:

        existing = (
            db.query(Venue)
            .filter(Venue.name == venue["name"])
            .first()
        )

        if existing:
            print(f"✓ {venue['name']} already exists")
            continue

        db.add(Venue(**venue))
        created += 1

    db.commit()

    print(f"\n{created} venue(s) created successfully.")