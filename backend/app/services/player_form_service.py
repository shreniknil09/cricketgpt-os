from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.player_form_repository import (
    get_batting_form,
    get_bowling_form,
)


def get_player_form(
    db: Session,
    player_id: int,
):
    """
    Calculate recent player form.
    """

    batting_records = get_batting_form(
        db,
        player_id,
    )

    bowling_records = get_bowling_form(
        db,
        player_id,
    )

    if not batting_records and not bowling_records:
        raise HTTPException(
            status_code=404,
            detail="No player statistics found.",
        )

    # ---------------------------------
    # Batting
    # ---------------------------------

    total_runs = sum(
        record.runs
        for record in batting_records
    )

    total_fours = sum(
        record.fours
        for record in batting_records
    )

    total_sixes = sum(
        record.sixes
        for record in batting_records
    )

    total_balls = sum(
        record.balls
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
    # Batting Form Score
    # ---------------------------------

    batting_score = 0.0

    batting_score += min(
        average_runs,
        60,
    )

    batting_score += min(
        total_fours * 0.5,
        10,
    )

    batting_score += min(
        total_sixes * 1.0,
        10,
    )

    if total_balls > 0:

        strike_rate = (
            total_runs
            / total_balls
            * 100
        )

        if strike_rate >= 140:

            batting_score += 20

        elif strike_rate >= 120:

            batting_score += 15

        elif strike_rate >= 100:

            batting_score += 8

    batting_score = min(
        batting_score,
        100,
    )

    # ---------------------------------
    # Bowling
    # ---------------------------------

    total_wickets = sum(
        record.wickets
        for record in bowling_records
    )

    total_runs_given = sum(
        record.runs_given
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
    # Bowling Form Score
    # ---------------------------------

    bowling_score = 0.0

    bowling_score += min(
        average_wickets * 20,
        60,
    )

    # Economy contribution
    if bowling_records:

        economy_values = [
            record.economy
            for record in bowling_records
            if record.economy > 0
        ]

        if economy_values:

            average_economy = (
                sum(economy_values)
                / len(economy_values)
            )

            if average_economy <= 6:

                bowling_score += 30

            elif average_economy <= 8:

                bowling_score += 20

            elif average_economy <= 10:

                bowling_score += 10

    bowling_score = min(
        bowling_score,
        100,
    )

    # ---------------------------------
    # Overall Form
    # ---------------------------------

    if batting_records and bowling_records:

        form_rating = (
            batting_score * 0.50
            + bowling_score * 0.50
        )

    elif batting_records:

        form_rating = batting_score

    else:

        form_rating = bowling_score

    form_rating = round(
        form_rating,
        2,
    )

    # ---------------------------------
    # Form Status
    # ---------------------------------

    if form_rating >= 80:

        form_status = "Excellent"

    elif form_rating >= 65:

        form_status = "Good"

    elif form_rating >= 50:

        form_status = "Average"

    elif form_rating >= 35:

        form_status = "Poor"

    else:

        form_status = "Very Poor"

    # ---------------------------------
    # Return
    # ---------------------------------

    return {
        "player_id": player_id,

        "matches": max(
            batting_matches,
            bowling_matches,
        ),

        "batting_score": round(
            batting_score,
            2,
        ),

        "bowling_score": round(
            bowling_score,
            2,
        ),

        "runs": total_runs,

        "wickets": total_wickets,

        "average_runs": round(
            average_runs,
            2,
        ),

        "average_wickets": round(
            average_wickets,
            2,
        ),

        "form_rating": form_rating,

        "form_status": form_status,
    }