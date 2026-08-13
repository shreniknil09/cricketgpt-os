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
# V5 Files
# ============================================================

TRAINING_DATA_PATH = (
    DATA_DIR
    / "match_training_data_v4.csv"
)

MODEL_PATH = (
    MODEL_DIR
    / "match_prediction_model_v5.joblib"
)

METRICS_PATH = (
    MODEL_DIR
    / "model_metrics_v5.json"
)


# ============================================================
# Target
# ============================================================

TARGET_COLUMN = "team1_win"


# ============================================================
# V5 Features
# ============================================================

FEATURE_COLUMNS = [

    "elo_difference",

    "win_rate_difference",

    "experience_difference",

    "venue_advantage",

    "head_to_head_difference",

    "form_10_difference",

    "form_5_difference",
]


# ============================================================
# Training Configuration
# ============================================================

TEST_SIZE = 0.20

RANDOM_STATE = 42

N_ESTIMATORS = 300

MINIMUM_TRAINING_ROWS = 20