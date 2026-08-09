from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.momentum_v2_repository import (
    get_current_innings,
    get_innings_balls,
)


RECENT_BALLS = 12


def get_momentum_v2(
    db: Session,
    match_id: int,
):
    innings = get_current_innings(
        db,
        match_id,
    )

    if innings is None:
        raise HTTPException(
            status_code=404,
            detail="No innings found for this match.",
        )

    balls = get_innings_balls(
        db,
        innings.id,
    )

    if not balls:
        raise HTTPException(
            status_code=404,
            detail="No ball data found for this innings.",
        )

    # ---------------------------------
    # Legal deliveries
    # ---------------------------------

    legal_balls = [
        ball
        for ball in balls
        if ball.extra_type not in [
            "Wide",
            "No Ball",
        ]
    ]

    if not legal_balls:
        raise HTTPException(
            status_code=400,
            detail="No legal deliveries available.",
        )

    # ---------------------------------
    # Recent and previous balls
    # ---------------------------------

    recent_balls = legal_balls[-RECENT_BALLS:]

    if len(legal_balls) >= RECENT_BALLS * 2:
        previous_balls = legal_balls[
            -(RECENT_BALLS * 2):-RECENT_BALLS
        ]
    else:
        previous_balls = legal_balls[
            :-RECENT_BALLS
        ]

    # ---------------------------------
    # Run Rate
    # ---------------------------------

    recent_runs = sum(
        ball.runs or 0
        for ball in recent_balls
    )

    previous_runs = sum(
        ball.runs or 0
        for ball in previous_balls
    )

    recent_run_rate = (
        recent_runs
        / (len(recent_balls) / 6)
        if recent_balls
        else 0
    )

    previous_run_rate = (
        previous_runs
        / (len(previous_balls) / 6)
        if previous_balls
        else recent_run_rate
    )

    run_rate_change = (
        recent_run_rate
        - previous_run_rate
    )

    # ---------------------------------
    # Boundaries
    # ---------------------------------

    recent_boundaries = sum(
        1
        for ball in recent_balls
        if (ball.runs or 0) in [4, 6]
    )

    previous_boundaries = sum(
        1
        for ball in previous_balls
        if (ball.runs or 0) in [4, 6]
    )

    boundary_difference = (
        recent_boundaries
        - previous_boundaries
    )

    # ---------------------------------
    # Dot balls
    # ---------------------------------

    recent_dot_balls = sum(
        1
        for ball in recent_balls
        if (ball.runs or 0) == 0
    )

    previous_dot_balls = sum(
        1
        for ball in previous_balls
        if (ball.runs or 0) == 0
    )

    dot_ball_difference = (
        recent_dot_balls
        - previous_dot_balls
    )

    # ---------------------------------
    # Wickets
    # ---------------------------------

    recent_wickets = sum(
        1
        for ball in recent_balls
        if ball.is_wicket
    )

    # ---------------------------------
    # Batting Momentum
    # ---------------------------------

    batting_score = (
        run_rate_change * 10
        + boundary_difference * 3
        - dot_ball_difference * 2
        - recent_wickets * 8
    )

    batting_momentum = (
        50 + batting_score
    )

    batting_momentum = max(
        0,
        min(
            batting_momentum,
            100,
        ),
    )

    # ---------------------------------
    # Bowling Momentum
    # ---------------------------------

    bowling_momentum = (
        100 - batting_momentum
    )

    # ---------------------------------
    # Momentum Status
    # ---------------------------------

    if batting_momentum >= 65:

        momentum_status = "Batting Dominant"

    elif batting_momentum >= 55:

        momentum_status = "Slight Batting Advantage"

    elif batting_momentum <= 35:

        momentum_status = "Bowling Dominant"

    elif batting_momentum <= 45:

        momentum_status = "Slight Bowling Advantage"

    else:

        momentum_status = "Balanced"

    # ---------------------------------
    # Response
    # ---------------------------------

    return {
        "match_id": match_id,
        "innings_id": innings.id,

        "batting_momentum": round(
            batting_momentum,
            2,
        ),

        "bowling_momentum": round(
            bowling_momentum,
            2,
        ),

        "run_rate_change": round(
            run_rate_change,
            2,
        ),

        "boundary_difference": (
            boundary_difference
        ),

        "dot_ball_difference": (
            dot_ball_difference
        ),

        "momentum_status": momentum_status,
    }