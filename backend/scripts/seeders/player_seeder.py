from app.models.player import Player
from app.models.team import Team


def seed_players(db):

    india = db.query(Team).filter(Team.short_name == "IND").first()
    australia = db.query(Team).filter(Team.short_name == "AUS").first()

    if not india or not australia:
        print("❌ Teams not found. Seed teams first.")
        return

    players = [
        # INDIA
        {
            "name": "Rohit Sharma",
            "batting_style": "Right-hand Bat",
            "bowling_style": "Right-arm Off Break",
            "role": "Batsman",
            "team_id": india.id,
        },
        {
            "name": "Shubman Gill",
            "batting_style": "Right-hand Bat",
            "bowling_style": "Right-arm Off Break",
            "role": "Batsman",
            "team_id": india.id,
        },
        {
            "name": "Virat Kohli",
            "batting_style": "Right-hand Bat",
            "bowling_style": "Right-arm Medium",
            "role": "Batsman",
            "team_id": india.id,
        },
        {
            "name": "KL Rahul",
            "batting_style": "Right-hand Bat",
            "bowling_style": "None",
            "role": "Wicketkeeper",
            "team_id": india.id,
        },
        {
            "name": "Hardik Pandya",
            "batting_style": "Right-hand Bat",
            "bowling_style": "Right-arm Fast Medium",
            "role": "All-Rounder",
            "team_id": india.id,
        },
        {
            "name": "Ravindra Jadeja",
            "batting_style": "Left-hand Bat",
            "bowling_style": "Left-arm Orthodox",
            "role": "All-Rounder",
            "team_id": india.id,
        },
        {
            "name": "Axar Patel",
            "batting_style": "Left-hand Bat",
            "bowling_style": "Left-arm Orthodox",
            "role": "All-Rounder",
            "team_id": india.id,
        },
        {
            "name": "Kuldeep Yadav",
            "batting_style": "Left-hand Bat",
            "bowling_style": "Left-arm Chinaman",
            "role": "Bowler",
            "team_id": india.id,
        },
        {
            "name": "Mohammed Shami",
            "batting_style": "Right-hand Bat",
            "bowling_style": "Right-arm Fast",
            "role": "Bowler",
            "team_id": india.id,
        },
        {
            "name": "Jasprit Bumrah",
            "batting_style": "Right-hand Bat",
            "bowling_style": "Right-arm Fast",
            "role": "Bowler",
            "team_id": india.id,
        },
        {
            "name": "Mohammed Siraj",
            "batting_style": "Right-hand Bat",
            "bowling_style": "Right-arm Fast",
            "role": "Bowler",
            "team_id": india.id,
        },

        # AUSTRALIA
        {
            "name": "David Warner",
            "batting_style": "Left-hand Bat",
            "bowling_style": "Right-arm Leg Break",
            "role": "Batsman",
            "team_id": australia.id,
        },
        {
            "name": "Travis Head",
            "batting_style": "Left-hand Bat",
            "bowling_style": "Right-arm Off Break",
            "role": "All-Rounder",
            "team_id": australia.id,
        },
        {
            "name": "Steve Smith",
            "batting_style": "Right-hand Bat",
            "bowling_style": "Right-arm Leg Break",
            "role": "Batsman",
            "team_id": australia.id,
        },
        {
            "name": "Marnus Labuschagne",
            "batting_style": "Right-hand Bat",
            "bowling_style": "Right-arm Leg Break",
            "role": "Batsman",
            "team_id": australia.id,
        },
        {
            "name": "Glenn Maxwell",
            "batting_style": "Right-hand Bat",
            "bowling_style": "Right-arm Off Break",
            "role": "All-Rounder",
            "team_id": australia.id,
        },
        {
            "name": "Marcus Stoinis",
            "batting_style": "Right-hand Bat",
            "bowling_style": "Right-arm Medium",
            "role": "All-Rounder",
            "team_id": australia.id,
        },
        {
            "name": "Alex Carey",
            "batting_style": "Left-hand Bat",
            "bowling_style": "None",
            "role": "Wicketkeeper",
            "team_id": australia.id,
        },
        {
            "name": "Pat Cummins",
            "batting_style": "Right-hand Bat",
            "bowling_style": "Right-arm Fast",
            "role": "Bowler",
            "team_id": australia.id,
        },
        {
            "name": "Mitchell Starc",
            "batting_style": "Left-hand Bat",
            "bowling_style": "Left-arm Fast",
            "role": "Bowler",
            "team_id": australia.id,
        },
        {
            "name": "Josh Hazlewood",
            "batting_style": "Left-hand Bat",
            "bowling_style": "Right-arm Fast",
            "role": "Bowler",
            "team_id": australia.id,
        },
        {
            "name": "Adam Zampa",
            "batting_style": "Right-hand Bat",
            "bowling_style": "Right-arm Leg Break",
            "role": "Bowler",
            "team_id": australia.id,
        },
    ]

    created = 0

    for player in players:

        existing = (
            db.query(Player)
            .filter(Player.name == player["name"])
            .first()
        )

        if existing:
            print(f"✓ {player['name']} already exists")
            continue

        db.add(Player(**player))
        created += 1

    db.commit()

    print(f"\n{created} player(s) created successfully.")