from app.database.session import SessionLocal
from app.models.team import Team
from app.models.player import Player


db = SessionLocal()

try:
    # -------------------------
    # Create Teams
    # -------------------------
    india = Team(
        name="India",
        short_name="IND",
        country="India",
    )

    australia = Team(
        name="Australia",
        short_name="AUS",
        country="Australia",
    )

    db.add(india)
    db.add(australia)
    db.commit()

    db.refresh(india)
    db.refresh(australia)

    print("Teams created successfully!")

    # -------------------------
    # India Players
    # -------------------------
    india_players = [
        "Rohit Sharma",
        "Shubman Gill",
        "Virat Kohli",
        "KL Rahul",
        "Hardik Pandya",
        "Ravindra Jadeja",
        "Axar Patel",
        "Kuldeep Yadav",
        "Mohammed Shami",
        "Jasprit Bumrah",
        "Mohammed Siraj",
    ]

    for player_name in india_players:
        db.add(
            Player(
                name=player_name,
                team_id=india.id,
            )
        )

    # -------------------------
    # Australia Players
    # -------------------------
    australia_players = [
        "David Warner",
        "Travis Head",
        "Steve Smith",
        "Marnus Labuschagne",
        "Glenn Maxwell",
        "Marcus Stoinis",
        "Alex Carey",
        "Pat Cummins",
        "Mitchell Starc",
        "Josh Hazlewood",
        "Adam Zampa",
    ]

    for player_name in australia_players:
        db.add(
            Player(
                name=player_name,
                team_id=australia.id,
            )
        )

    db.commit()

    print("22 Players created successfully!")

finally:
    db.close()