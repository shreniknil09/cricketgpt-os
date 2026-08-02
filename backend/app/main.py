from fastapi import FastAPI

from app.api.team_routes import router as team_router
from app.api.player_routes import router as player_router
from app.api.auth_routes import router as auth_router
from app.api.venue_routes import router as venue_router
from app.api.tournament_routes import router as tournament_router
from app.api.match_routes import router as match_router

app = FastAPI(
    title="CricketGPT OS",
    version="1.0.0"
)

# Register all routes
app.include_router(team_router)
app.include_router(player_router)
app.include_router(auth_router)
app.include_router(venue_router)
app.include_router(tournament_router)
app.include_router(match_router)

@app.get("/")
def root():
    return {
        "message": "Welcome to CricketGPT OS"
    }