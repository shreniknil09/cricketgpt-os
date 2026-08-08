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
from app.api.player_of_match_routes import (
    router as player_of_match_router,
)
from app.api.partnership_routes import (
    router as partnership_router,
)
from app.api.fall_of_wickets_routes import (
    router as fall_of_wickets_router,
)
from app.api.player_impact_routes import (
    router as player_impact_router,
)
from app.api.win_probability_routes import (
    router as win_probability_router,
)
from app.api.match_situation_routes import (
    router as match_situation_router,
)
from app.api.momentum_routes import (
    router as momentum_router,
)
from app.api.match_prediction_routes import (
    router as match_prediction_router,
)
from app.api.team_strength_routes import (
    router as team_strength_router,
)
from app.api.player_form_routes import (
    router as player_form_router,
)
from app.api.team_form_routes import (
    router as team_form_router,
)
from app.api.venue_analysis_routes import (
    router as venue_analysis_router,
)
from app.api.head_to_head_routes import (
    router as head_to_head_router,
)
from app.api.match_prediction_v2_routes import (
    router as match_prediction_v2_router,
)
from app.api.ml_prediction_routes import (
    router as ml_prediction_router,
)
from app.api.ml_prediction_v2_routes import (
    router as ml_prediction_v2_router,
)
from app.api.score_prediction_routes import (
    router as score_prediction_router,
)
from app.api.player_performance_routes import (
    router as player_performance_router,
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
app.include_router(player_of_match_router)
app.include_router(partnership_router)  
app.include_router(fall_of_wickets_router)
app.include_router(player_impact_router)  
app.include_router(win_probability_router)  
app.include_router(match_situation_router)  
app.include_router(momentum_router) 
app.include_router(match_prediction_router) 
app.include_router(team_strength_router)   
app.include_router(player_form_router)   
app.include_router(team_form_router)    
app.include_router(venue_analysis_router)
app.include_router(head_to_head_router)
app.include_router(match_prediction_v2_router)      
app.include_router(ml_prediction_router)     
app.include_router(ml_prediction_v2_router)  
app.include_router(score_prediction_router) 
app.include_router(player_performance_router)   

@app.get("/")
def root():
    return {
        "message": "Welcome to CricketGPT OS",
        "version": "1.0.0",
        "docs": "/docs",
    }