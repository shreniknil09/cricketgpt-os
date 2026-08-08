from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.player_performance_repository import (
    get_recent_batting_stats,
    get_recent_bowling_stats,
)


def get_player_performance(
    db: Session,
    player_id: int,
):
    """
    Predict expected player performance
    using recent historical statistics.
    """

    batting_records = get_recent_batting_stats(
        db,
        player_id,
    )

    bowling_records = get_recent_bowling_stats(
        db,
        player_id,
    )

    if not batting_records and not bowling_records:
        raise HTTPException(
            status_code=404,
            detail="No player performance data found.",
        )

    # ---------------------------------
    # Batting Statistics
    # ---------------------------------

    total_runs = sum(
        record.runs or 0
        for record in batting_records
    )

    total_balls = sum(
        record.balls or 0
        for record in batting_records
    )

    batting_matches = len(
        batting_records
    )

    if batting_matches > 0:

        average_runs = (
            total_runs
            / batting_matches
        )

    else:

        average_runs = 0.0

    # ---------------------------------
    # Recent Batting Performance
    # ---------------------------------

    if batting_records:

        recent_runs = sum(
            record.runs or 0
            for record in batting_records[:3]
        )

        recent_matches = min(
            len(batting_records),
            3,
        )

        recent_average = (
            recent_runs
            / recent_matches
        )

    else:

        recent_average = 0.0

    # ---------------------------------
    # Expected Runs
    # ---------------------------------

    expected_runs = (
        average_runs * 0.60
        + recent_average * 0.40
    )

    # ---------------------------------
    # Bowling Statistics
    # ---------------------------------

    total_wickets = sum(
        record.wickets or 0
        for record in bowling_records
    )

    bowling_matches = len(
        bowling_records
    )

    if bowling_matches > 0:

        average_wickets = (
            total_wickets
            / bowling_matches
        )

    else:

        average_wickets = 0.0

    # ---------------------------------
    # Recent Bowling Performance
    # ---------------------------------

    if bowling_records:

        recent_wickets = sum(
            record.wickets or 0
            for record in bowling_records[:3]
        )

        recent_bowling_matches = min(
            len(bowling_records),
            3,
        )

        recent_wicket_average = (
            recent_wickets
            / recent_bowling_matches
        )

    else:

        recent_wicket_average = 0.0

    # ---------------------------------
    # Expected Wickets
    # ---------------------------------

    expected_wickets = (
        average_wickets * 0.60
        + recent_wicket_average * 0.40
    )

    # ---------------------------------
    # Performance Rating
    # ---------------------------------

    batting_component = min(
        expected_runs,
        60,
    )

    bowling_component = min(
        expected_wickets * 20,
        40,
    )

    performance_rating = (
        batting_component
        + bowling_component
    )

    # ---------------------------------
    # Normalize
    # ---------------------------------

    performance_rating = max(
        0.0,
        min(
            performance_rating,
            100.0,
        ),
    )

    # ---------------------------------
    # Performance Status
    # ---------------------------------

    if performance_rating >= 80:

        performance_status = "Excellent"

    elif performance_rating >= 65:

        performance_status = "Good"

    elif performance_rating >= 50:

        performance_status = "Average"

    elif performance_rating >= 35:

        performance_status = "Poor"

    else:

        performance_status = "Very Poor"

    # ---------------------------------
    # Match Count
    # ---------------------------------

    matches = max(
        batting_matches,
        bowling_matches,
    )

    # ---------------------------------
    # Return
    # ---------------------------------

    return {
        "player_id": player_id,

        "matches": matches,

        "expected_runs": int(
            round(expected_runs)
        ),

        "expected_wickets": int(
            round(expected_wickets)
        ),

        "average_runs": round(
            average_runs,
            2,
        ),

        "average_wickets": round(
            average_wickets,
            2,
        ),

        "performance_rating": round(
            performance_rating,
            2,
        ),

        "performance_status": (
            performance_status
        ),
    }