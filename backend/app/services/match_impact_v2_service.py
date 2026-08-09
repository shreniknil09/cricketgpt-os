from fastapi import HTTPException

from app.repositories.match_impact_v2_repository import (
    get_match,
    get_match_player_stats,
)

from app.services.team_strength_service import (
    get_team_strength,
)

from app.services.team_form_service import (
    get_team_form,
)


def _safe_strength(
    db,
    team_id,
):
    try:
        result = get_team_strength(
            db,
            team_id,
        )

        return result.get(
            "overall_strength",
            50,
        )

    except Exception:
        return 50.0


def _safe_form(
    db,
    team_id,
):
    try:
        result = get_team_form(
            db,
            team_id,
        )

        return result.get(
            "form_rating",
            50,
        )

    except Exception:
        return 50.0


def get_match_impact_v2(
    db,
    match_id: int,
):
    match = get_match(
        db,
        match_id,
    )

    if match is None:
        raise HTTPException(
            status_code=404,
            detail="Match not found.",
        )

    player_stats = get_match_player_stats(
        db,
        match_id,
    )

    team1_strength = _safe_strength(
        db,
        match.team1_id,
    )

    team2_strength = _safe_strength(
        db,
        match.team2_id,
    )

    team1_form = _safe_form(
        db,
        match.team1_id,
    )

    team2_form = _safe_form(
        db,
        match.team2_id,
    )

    team1_player_impact = 0.0
    team2_player_impact = 0.0

    for stat in player_stats:

        runs = getattr(
            stat,
            "runs",
            0,
        ) or 0

        wickets = getattr(
            stat,
            "wickets",
            0,
        ) or 0

        impact = (
            min(runs, 100) * 0.5
            + min(wickets * 20, 50)
        )

        # Use team_id if available.
        player_team_id = getattr(
            stat,
            "team_id",
            None,
        )

        if player_team_id == match.team1_id:
            team1_player_impact += impact

        elif player_team_id == match.team2_id:
            team2_player_impact += impact

    team1_player_impact = min(
        team1_player_impact,
        100,
    )

    team2_player_impact = min(
        team2_player_impact,
        100,
    )

    team1_impact = (
        team1_strength * 0.35
        + team1_form * 0.30
        + team1_player_impact * 0.35
    )

    team2_impact = (
        team2_strength * 0.35
        + team2_form * 0.30
        + team2_player_impact * 0.35
    )

    team1_impact = max(
        0,
        min(team1_impact, 100),
    )

    team2_impact = max(
        0,
        min(team2_impact, 100),
    )

    difference = (
        team1_impact
        - team2_impact
    )

    if abs(difference) < 5:
        dominant_team = None
        status = "Balanced"

    elif difference > 0:
        dominant_team = match.team1_id

        status = (
            "Strong Team 1 Advantage"
            if difference >= 15
            else "Team 1 Advantage"
        )

    else:
        dominant_team = match.team2_id

        status = (
            "Strong Team 2 Advantage"
            if abs(difference) >= 15
            else "Team 2 Advantage"
        )

    return {
        "match_id": match_id,
        "team1_id": match.team1_id,
        "team2_id": match.team2_id,
        "team1_impact": round(
            team1_impact,
            2,
        ),
        "team2_impact": round(
            team2_impact,
            2,
        ),
        "impact_difference": round(
            abs(difference),
            2,
        ),
        "dominant_team_id": dominant_team,
        "impact_status": status,
    }