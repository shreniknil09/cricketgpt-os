from fastapi import HTTPException

from app.repositories.partnership_v2_repository import (
    get_innings,
    get_partnerships,
)


def get_partnership_analysis(
    db,
    match_id: int,
):
    innings = get_innings(
        db,
        match_id,
    )

    if innings is None:
        raise HTTPException(
            status_code=404,
            detail="No innings found for this match.",
        )

    partnerships = get_partnerships(
        db,
        innings.id,
    )

    if not partnerships:
        raise HTTPException(
            status_code=404,
            detail="No partnership data found.",
        )

    partnership_runs = [
        partnership["runs"]
        for partnership in partnerships
    ]

    total_runs = sum(
        partnership_runs
    )

    highest_partnership = max(
        partnership_runs
    )

    average_partnership = (
        total_runs
        / len(partnership_runs)
    )

    strongest = max(
        partnerships,
        key=lambda partnership: partnership["runs"],
    )

    strongest_partnership = (
        f"Player {strongest['striker_id']} "
        f"& Player {strongest['non_striker_id']} "
        f"- {strongest['runs']} runs"
    )

    return {
        "match_id": match_id,
        "innings_id": innings.id,

        "partnership_count": len(
            partnerships
        ),

        "total_partnership_runs": total_runs,

        "highest_partnership": highest_partnership,

        "average_partnership": round(
            average_partnership,
            2,
        ),

        "strongest_partnership":
            strongest_partnership,
    }