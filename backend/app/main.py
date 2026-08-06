from fastapi import FastAPI

from app.api.auth_routes import router as auth_router
from app.api.team_routes import router as team_router
from app.api.player_routes import router as player_router
from app.api.venue_routes import router as venue_router
from app.api.tournament_routes import router as tournament_router
from app.api.match_routes import router as match_router
from app.api.playing_xi_routes import router as playing_xi_router
from app.api.toss_routes import router as toss_router
from app.api.innings_routes import router as innings_router
from app.api.over_routes import router as over_router
from app.api.ball_routes import router as ball_router
from app.api.player_match_stats_routes import (
    router as player_match_stats_router,
)
from app.api.bowler_match_stats_routes import (
    router as bowler_match_stats_router,
)
from app.api.live_score_routes import (
    router as live_score_router,
)
from app.api.scorecard_routes import (
    router as scorecard_router,
)
from app.api.match_summary_routes import (
    router as match_summary_router,
)
from app.api.commentary_routes import (
    router as commentary_router,
)
from app.api.points_table_routes import (
    router as points_table_router,
)
from app.api.player_career_routes import (
    router as player_career_router,
)
from app.api.leaderboard_routes import (
    router as leaderboard_router,
)
from app.api.team_stats_routes import (
    router as team_stats_router,
)

app = FastAPI(
    title="CricketGPT OS",
    version="1.0.0",
)

# ---------------------------------------
# Register All API Routes
# ---------------------------------------

app.include_router(auth_router)
app.include_router(team_router)
app.include_router(player_router)
app.include_router(venue_router)
app.include_router(tournament_router)
app.include_router(match_router)
app.include_router(playing_xi_router)
app.include_router(toss_router)
app.include_router(innings_router)
app.include_router(over_router)
app.include_router(ball_router)
app.include_router(player_match_stats_router)
app.include_router(bowler_match_stats_router)
app.include_router(live_score_router)
app.include_router(scorecard_router)
app.include_router(match_summary_router)
app.include_router(commentary_router)
app.include_router(points_table_router)
app.include_router(player_career_router)
app.include_router(leaderboard_router)
app.include_router(team_stats_router)

@app.get("/")
def root():
    return {
        "message": "Welcome to CricketGPT OS",
        "version": "1.0.0",
        "docs": "/docs",
    }