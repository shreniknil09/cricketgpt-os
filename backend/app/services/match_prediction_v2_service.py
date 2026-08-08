from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.match_prediction_v2_repository import (
    get_match,
)

from app.services.team_strength_service import (
    get_team_strength,
)

from app.services.team_form_service import (
    get_team_form,
)

from app.services.venue_analysis_service import (
    get_venue_analysis,
)

from app.services.head_to_head_service import (
    get_head_to_head,
)


def get_match_prediction_v2(
    db: Session,
    match_id: int,
):
    """
    Generate an advanced rule-based match prediction.

    Uses:
    - Team Strength
    - Team Form
    - Venue Performance
    - Head-to-Head
    - Toss
    """

    # ---------------------------------
    # Get Match
    # ---------------------------------

    match = get_match(
        db,
        match_id,
    )

    if match is None:
        raise HTTPException(
            status_code=404,
            detail="Match not found.",
        )

    team1_id = match.team1_id
    team2_id = match.team2_id
    venue_id = match.venue_id

    # ---------------------------------
    # Team Strength
    # ---------------------------------

    team1_strength = get_team_strength(
        db,
        team1_id,
    )

    team2_strength = get_team_strength(
        db,
        team2_id,
    )

    # ---------------------------------
    # Team Form
    # ---------------------------------

    team1_form = get_team_form(
        db,
        team1_id,
    )

    team2_form = get_team_form(
        db,
        team2_id,
    )

    # ---------------------------------
    # Venue Analysis
    # ---------------------------------

    team1_venue = 50.0
    team2_venue = 50.0

    try:

        venue1 = get_venue_analysis(
            db,
            team1_id,
            venue_id,
        )

        team1_venue = venue1[
            "venue_rating"
        ]

    except HTTPException:

        pass

    try:

        venue2 = get_venue_analysis(
            db,
            team2_id,
            venue_id,
        )

        team2_venue = venue2[
            "venue_rating"
        ]

    except HTTPException:

        pass

    # ---------------------------------
    # Head-to-Head
    # ---------------------------------

    team1_h2h = 50.0
    team2_h2h = 50.0

    try:

        h2h = get_head_to_head(
            db,
            team1_id,
            team2_id,
        )

        team1_h2h = h2h[
            "team1_win_rate"
        ]

        team2_h2h = h2h[
            "team2_win_rate"
        ]

    except HTTPException:

        pass

    # ---------------------------------
    # Calculate Component Scores
    # ---------------------------------

    team1_score = (
        team1_strength[
            "overall_strength"
        ] * 0.35
        + team1_form[
            "form_rating"
        ] * 0.25
        + team1_venue * 0.15
        + team1_h2h * 0.15
    )

    team2_score = (
        team2_strength[
            "overall_strength"
        ] * 0.35
        + team2_form[
            "form_rating"
        ] * 0.25
        + team2_venue * 0.15
        + team2_h2h * 0.15
    )

    # ---------------------------------
    # Toss Impact
    # ---------------------------------

    if match.toss_winner_id == team1_id:

        team1_score += 5.0

    elif match.toss_winner_id == team2_id:

        team2_score += 5.0

    # ---------------------------------
    # Normalize
    # ---------------------------------

    total_score = (
        team1_score
        + team2_score
    )

    if total_score <= 0:

        team1_probability = 50.0
        team2_probability = 50.0

    else:

        team1_probability = (
            team1_score
            / total_score
            * 100
        )

        team2_probability = (
            team2_score
            / total_score
            * 100
        )

    # ---------------------------------
    # Predicted Winner
    # ---------------------------------

    if (
        team1_probability
        >= team2_probability
    ):

        predicted_winner_id = team1_id

    else:

        predicted_winner_id = team2_id

    # ---------------------------------
    # Return
    # ---------------------------------

    return {
        "match_id": match_id,

        "team1_id": team1_id,
        "team2_id": team2_id,

        "team1_score": round(
            team1_score,
            2,
        ),

        "team2_score": round(
            team2_score,
            2,
        ),

        "team1_probability": round(
            team1_probability,
            2,
        ),

        "team2_probability": round(
            team2_probability,
            2,
        ),

        "predicted_winner_id": (
            predicted_winner_id
        ),
    }