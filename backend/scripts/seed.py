import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.session import SessionLocal

from scripts.seeders.team_seeder import seed_teams
from scripts.seeders.player_seeder import seed_players
from scripts.seeders.venue_seeder import seed_venues
from scripts.seeders.tournament_seeder import seed_tournaments
from scripts.seeders.match_seeder import seed_matches

def run_seed():
    db = SessionLocal()

    try:
        print("=" * 50)
        print("CricketGPT OS Database Seeder")
        print("=" * 50)

        print("\nSeeding Teams...")
        seed_teams(db)

        print("\nSeeding Players...")
        seed_players(db)
    
        print("\nSeeding Venues...")
        seed_venues(db)
    
        print("\nSeeding Tournaments...")
        seed_tournaments(db)
    
        print("\nSeeding Matches...")
        seed_matches(db)
            
        print("\nDatabase seeding completed successfully!")

    except Exception as e:
        db.rollback()
        print(f"\nError: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    run_seed()