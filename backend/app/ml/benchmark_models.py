from pathlib import Path
import json

import pandas as pd

from sklearn.ensemble import (
    RandomForestClassifier,
    GradientBoostingClassifier,
)

from sklearn.linear_model import LogisticRegression

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
)

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


# ============================================================
# Paths
# ============================================================

BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

DATA_PATH = (
    BASE_DIR
    / "data"
    / "ml"
    / "match_training_data_v4.csv"
)

OUTPUT_PATH = (
    BASE_DIR
    / "models"
    / "ml"
    / "benchmark_results.json"
)


# ============================================================
# Configuration
# ============================================================

TEST_SIZE = 0.20

RANDOM_STATE = 42

FEATURE_COLUMNS = [
    "elo_difference",
    "form_5_difference",
    "form_10_difference",
    "win_rate_difference",
    "run_rate_difference",
    "boundary_rate_difference",
    "bowling_run_rate_difference",
    "wickets_difference",
    "wickets_per_ball_difference",
    "head_to_head_difference",
    "venue_advantage",
    "experience_difference",
]

TARGET_COLUMN = "team1_win"


# ============================================================
# Load Dataset
# ============================================================

def load_dataset():

    if not DATA_PATH.exists():

        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}"
        )

    dataframe = pd.read_csv(
        DATA_PATH
    )

    required_columns = (
        FEATURE_COLUMNS
        + [
            TARGET_COLUMN,
            "match_date",
        ]
    )

    missing = [
        column
        for column in required_columns
        if column not in dataframe.columns
    ]

    if missing:

        raise ValueError(
            "Missing columns: "
            + ", ".join(missing)
        )

    dataframe["match_date"] = (
        pd.to_datetime(
            dataframe["match_date"],
            errors="coerce",
        )
    )

    dataframe = dataframe.dropna(
        subset=required_columns
    )

    dataframe = dataframe.sort_values(
        "match_date"
    ).reset_index(
        drop=True
    )

    if len(dataframe) < 20:

        raise ValueError(
            "At least 20 valid matches "
            "are required."
        )

    if dataframe[
        TARGET_COLUMN
    ].nunique() < 2:

        raise ValueError(
            "Target must contain both "
            "classes."
        )

    return dataframe


# ============================================================
# Metrics
# ============================================================

def evaluate_model(
    model,
    X_test,
    y_test,
):

    predictions = model.predict(
        X_test
    )

    probabilities = (
        model.predict_proba(
            X_test
        )[:, 1]
    )

    return {

        "accuracy":
            round(
                accuracy_score(
                    y_test,
                    predictions,
                ),
                4,
            ),

        "precision":
            round(
                precision_score(
                    y_test,
                    predictions,
                    zero_division=0,
                ),
                4,
            ),

        "recall":
            round(
                recall_score(
                    y_test,
                    predictions,
                    zero_division=0,
                ),
                4,
            ),

        "f1_score":
            round(
                f1_score(
                    y_test,
                    predictions,
                    zero_division=0,
                ),
                4,
            ),

        "roc_auc":
            round(
                roc_auc_score(
                    y_test,
                    probabilities,
                ),
                4,
            ),

        "confusion_matrix":
            confusion_matrix(
                y_test,
                predictions,
            ).tolist(),
    }


# ============================================================
# Model Definitions
# ============================================================

def create_models():

    models = {

        "LogisticRegression":
            Pipeline(
                [
                    (
                        "scaler",
                        StandardScaler(),
                    ),
                    (
                        "classifier",
                        LogisticRegression(
                            random_state=(
                                RANDOM_STATE
                            ),
                            max_iter=2000,
                        ),
                    ),
                ]
            ),

        "RandomForestClassifier":
            Pipeline(
                [
                    (
                        "scaler",
                        StandardScaler(),
                    ),
                    (
                        "classifier",
                        RandomForestClassifier(
                            n_estimators=300,
                            random_state=(
                                RANDOM_STATE
                            ),
                            class_weight="balanced",
                            n_jobs=-1,
                        ),
                    ),
                ]
            ),

        "GradientBoostingClassifier":
            Pipeline(
                [
                    (
                        "scaler",
                        StandardScaler(),
                    ),
                    (
                        "classifier",
                        GradientBoostingClassifier(
                            n_estimators=200,
                            learning_rate=0.05,
                            max_depth=3,
                            random_state=(
                                RANDOM_STATE
                            ),
                        ),
                    ),
                ]
            ),
    }

    return models


# ============================================================
# Benchmark
# ============================================================

def benchmark_models():

    print(
        "Starting CricketGPT model benchmark..."
    )

    dataframe = load_dataset()

    print(
        f"Dataset rows: {len(dataframe)}"
    )

    # ========================================================
    # Chronological split
    # ========================================================

    split_index = int(
        len(dataframe)
        * (1 - TEST_SIZE)
    )

    train_df = dataframe.iloc[
        :split_index
    ]

    test_df = dataframe.iloc[
        split_index:
    ]

    X_train = train_df[
        FEATURE_COLUMNS
    ]

    y_train = train_df[
        TARGET_COLUMN
    ]

    X_test = test_df[
        FEATURE_COLUMNS
    ]

    y_test = test_df[
        TARGET_COLUMN
    ]

    print()

    print(
        "Chronological split:"
    )

    print(
        f"Training samples: "
        f"{len(train_df)}"
    )

    print(
        f"Test samples: "
        f"{len(test_df)}"
    )

    print(
        f"Training period: "
        f"{train_df['match_date'].min().date()} "
        f"to "
        f"{train_df['match_date'].max().date()}"
    )

    print(
        f"Testing period: "
        f"{test_df['match_date'].min().date()} "
        f"to "
        f"{test_df['match_date'].max().date()}"
    )

    # ========================================================
    # Train models
    # ========================================================

    models = create_models()

    results = {}

    print()

    print(
        "=========================================="
    )

    print(
        "MODEL BENCHMARK"
    )

    print(
        "=========================================="
    )

    for name, model in models.items():

        print()

        print(
            f"Training {name}..."
        )

        model.fit(
            X_train,
            y_train,
        )

        metrics = evaluate_model(
            model,
            X_test,
            y_test,
        )

        results[name] = metrics

        print(
            f"Accuracy : "
            f"{metrics['accuracy']:.4f}"
        )

        print(
            f"Precision: "
            f"{metrics['precision']:.4f}"
        )

        print(
            f"Recall   : "
            f"{metrics['recall']:.4f}"
        )

        print(
            f"F1 Score : "
            f"{metrics['f1_score']:.4f}"
        )

        print(
            f"ROC-AUC  : "
            f"{metrics['roc_auc']:.4f}"
        )

        print(
            "Confusion Matrix:"
        )

        print(
            metrics[
                "confusion_matrix"
            ]
        )

    # ========================================================
    # Determine best model
    # ========================================================

    best_model = max(
        results,
        key=lambda name:
            results[name][
                "roc_auc"
            ],
    )

    # ========================================================
    # Save results
    # ========================================================

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output = {

        "dataset_rows":
            len(dataframe),

        "training_rows":
            len(train_df),

        "test_rows":
            len(test_df),

        "training_start":
            str(
                train_df[
                    "match_date"
                ].min().date()
            ),

        "training_end":
            str(
                train_df[
                    "match_date"
                ].max().date()
            ),

        "testing_start":
            str(
                test_df[
                    "match_date"
                ].min().date()
            ),

        "testing_end":
            str(
                test_df[
                    "match_date"
                ].max().date()
            ),

        "feature_count":
            len(FEATURE_COLUMNS),

        "features":
            FEATURE_COLUMNS,

        "models":
            results,

        "best_model":
            best_model,
    }

    with OUTPUT_PATH.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            output,
            file,
            indent=4,
        )

    print()

    print(
        "=========================================="
    )

    print(
        f"Best model by ROC-AUC: "
        f"{best_model}"
    )

    print(
        "=========================================="
    )

    print()

    print(
        "Benchmark results saved at:"
    )

    print(
        OUTPUT_PATH
    )

    return results


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":

    benchmark_models()