from sqlalchemy.orm import Session

from app.database.session import SessionLocal

from app.ml.historical_feature_extractor import (
    extract_base_training_records,
)


def build_dataset():
    db: Session = SessionLocal()

    try:

        records = extract_base_training_records(
            db
        )

        print(
            f"Completed matches found: {len(records)}"
        )

        if not records:
            print(
                "No completed matches with "
                "winner data were found."
            )

            return

        print(
            "\nBase historical records:"
        )

        for record in records[:10]:

            print(
                record
            )

        if len(records) > 10:

            print(
                f"\n... and "
                f"{len(records) - 10} more."
            )

    finally:

        db.close()


if __name__ == "__main__":
    build_dataset()