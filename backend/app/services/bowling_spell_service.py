from fastapi import HTTPException

from app.repositories.bowling_spell_repository import (
    get_player_bowling_stats,
)


def get_bowling_spell(
    db,
    player_id: int,
):
    records = get_player_bowling_stats(
        db,
        player_id,
    )

    if not records:
        raise HTTPException(
            status_code=404,
            detail="No bowling statistics found.",
        )

    total_overs = sum(
        record.overs or 0
        for record in records
    )

    total_runs = sum(
        record.runs_conceded or 0
        for record in records
    )

    total_wickets = sum(
        record.wickets or 0
        for record in records
    )

    matches = len(records)

    average_economy = (
        total_runs / total_overs
        if total_overs
        else 0
    )

    average_wickets = (
        total_wickets / matches
        if matches
        else 0
    )

    economy_score = max(
        0,
        100 - average_economy * 8,
    )

    wicket_score = min(
        average_wickets * 20,
        60,
    )

    rating = (
        economy_score * 0.4
        + wicket_score * 0.6
    )

    rating = max(
        0,
        min(rating, 100),
    )

    if rating >= 80:
        status = "Excellent"
    elif rating >= 65:
        status = "Good"
    elif rating >= 50:
        status = "Average"
    elif rating >= 35:
        status = "Poor"
    else:
        status = "Very Poor"

    return {
        "player_id": player_id,
        "matches": matches,
        "total_overs": round(total_overs, 2),
        "total_runs_given": total_runs,
        "total_wickets": total_wickets,
        "average_economy": round(
            average_economy,
            2,
        ),
        "average_wickets": round(
            average_wickets,
            2,
        ),
        "spell_rating": round(
            rating,
            2,
        ),
        "spell_status": status,
    }