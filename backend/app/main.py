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

app = FastAPI(
    title="CricketGPT OS",
    version="1.0.0",
)

# Register all routes
app.include_router(auth_router)
app.include_router(team_router)
app.include_router(player_router)
app.include_router(venue_router)
app.include_router(tournament_router)
app.include_router(match_router)
app.include_router(playing_xi_router)
app.include_router(toss_router)
app.include_router(innings_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to CricketGPT OS"
    }