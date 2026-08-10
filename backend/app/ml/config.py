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

ML_DIR = BASE_DIR / "app" / "ml"

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
# Files
# ============================================================

TRAINING_DATA_PATH = (
    DATA_DIR
    / "match_training_data.csv"
)

MODEL_PATH = (
    MODEL_DIR
    / "match_prediction_model.joblib"
)

METRICS_PATH = (
    MODEL_DIR
    / "model_metrics.json"
)


# ============================================================
# Target
# ============================================================

TARGET_COLUMN = "team1_win"


# ============================================================
# V3 Pre-Match ML Features
# ============================================================

FEATURE_COLUMNS = [

    # --------------------------------------------------------
    # Overall Team Strength
    # --------------------------------------------------------

    "elo_difference",

    # --------------------------------------------------------
    # Batting Performance
    # --------------------------------------------------------

    "run_rate_difference",

    "boundary_rate_difference",

    "dot_ball_rate_difference",

    # --------------------------------------------------------
    # Bowling Performance
    # --------------------------------------------------------

    "runs_conceded_difference",

    "wickets_difference",

    "bowling_run_rate_difference",

    "wickets_per_ball_difference",

    # --------------------------------------------------------
    # Recent Team Performance
    # --------------------------------------------------------

    "win_rate_difference",

    "form_difference",
]


# ============================================================
# Training Configuration
# ============================================================

TEST_SIZE = 0.20

RANDOM_STATE = 42

N_ESTIMATORS = 300

MINIMUM_TRAINING_ROWS = 20