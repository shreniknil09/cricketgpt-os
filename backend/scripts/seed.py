print("Seed file started")

from app.database.session import SessionLocal

from scripts.seeders.team_seeder import seed_teams


def run_seed():
    db = SessionLocal()

    try:
        print("=" * 50)
        print("CricketGPT OS Database Seeder")
        print("=" * 50)

        seed_teams(db)

        print("\nDatabase seeding completed successfully!")

    except Exception as e:
        db.rollback()
        print(f"\nError: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    print("Calling run_seed()...")
    run_seed()
    print("Finished run_seed()")