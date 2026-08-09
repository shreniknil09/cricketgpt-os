from pathlib import Path


# ---------------------------------
# Project Paths
# ---------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent.parent

ML_DIR = BASE_DIR / "app" / "ml"
DATA_DIR = BASE_DIR / "app" / "data" / "ml"
MODEL_DIR = BASE_DIR / "app" / "models" / "ml"


# ---------------------------------
# Files
# ---------------------------------

TRAINING_DATA_PATH = DATA_DIR / "match_training_data.csv"

MODEL_PATH = MODEL_DIR / "match_prediction_model.joblib"

METRICS_PATH = MODEL_DIR / "model_metrics.json"


# ---------------------------------
# Target
# ---------------------------------

TARGET_COLUMN = "team1_win"


# ---------------------------------
# ML Features
# ---------------------------------

FEATURE_COLUMNS = [
    "team1_strength",
    "team2_strength",
    "team1_form",
    "team2_form",
    "team1_player_form",
    "team2_player_form",
    "venue_advantage",
    "head_to_head_advantage",
    "momentum",
    "pressure_index",
    "run_rate",
    "required_run_rate",
    "chase_difficulty",
    "match_impact",
]


# ---------------------------------
# Training Configuration
# ---------------------------------

TEST_SIZE = 0.20

RANDOM_STATE = 42

N_ESTIMATORS = 300

MINIMUM_TRAINING_ROWS = 20