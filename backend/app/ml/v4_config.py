from pathlib import Path


# ============================================================
# Project Paths
# ============================================================

BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
    .parent
)

DATA_DIR = (
    BASE_DIR
    / "app"
    / "data"
    / "ml"
)

MODEL_DIR = (
    BASE_DIR
    / "app"
    / "models"
    / "ml"
)


# ============================================================
# V4 Files
# ============================================================

TRAINING_DATA_PATH = (
    DATA_DIR
    / "match_training_data_v4.csv"
)

MODEL_PATH = (
    MODEL_DIR
    / "match_prediction_model_v4.joblib"
)

METRICS_PATH = (
    MODEL_DIR
    / "model_metrics_v4.json"
)


# ============================================================
# Target
# ============================================================

TARGET_COLUMN = "team1_win"


# ============================================================
# V4 Feature Columns
# ============================================================

FEATURE_COLUMNS = [

    # Elo
    "elo_difference",

    # Recent form
    "form_5_difference",
    "form_10_difference",

    # Historical win rate
    "win_rate_difference",

    # Batting
    "run_rate_difference",
    "boundary_rate_difference",

    # Bowling
    "bowling_run_rate_difference",
    "wickets_difference",
    "wickets_per_ball_difference",

    # Head-to-head
    "head_to_head_difference",

    # Venue
    "venue_advantage",

    # Experience
    "experience_difference",
]


# ============================================================
# Training Configuration
# ============================================================

TEST_SIZE = 0.20

RANDOM_STATE = 42

N_ESTIMATORS = 300

MINIMUM_TRAINING_ROWS = 20