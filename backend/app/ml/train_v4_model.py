from datetime import datetime
import json

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
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

from app.ml.v4_config import (
    FEATURE_COLUMNS,
    TARGET_COLUMN,
    TRAINING_DATA_PATH,
    MODEL_PATH,
    METRICS_PATH,
    TEST_SIZE,
    RANDOM_STATE,
    N_ESTIMATORS,
    MINIMUM_TRAINING_ROWS,
)


# ============================================================
# Load Dataset
# ============================================================

def load_dataset():

    if not TRAINING_DATA_PATH.exists():
        raise FileNotFoundError(
            f"V4 training dataset not found: "
            f"{TRAINING_DATA_PATH}"
        )

    dataframe = pd.read_csv(
        TRAINING_DATA_PATH
    )

    required_columns = (
        FEATURE_COLUMNS
        + [TARGET_COLUMN]
        + [
            "match_date",
            "match_id",
            "team1",
            "team2",
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

    # Convert date safely
    dataframe["match_date"] = pd.to_datetime(
        dataframe["match_date"],
        errors="coerce",
    )

    # Remove invalid rows
    dataframe = dataframe.dropna(
        subset=FEATURE_COLUMNS
        + [
            TARGET_COLUMN,
            "match_date",
        ]
    )

    if len(dataframe) < MINIMUM_TRAINING_ROWS:
        raise ValueError(
            f"At least "
            f"{MINIMUM_TRAINING_ROWS} "
            f"valid matches are required."
        )

    if dataframe[TARGET_COLUMN].nunique() < 2:
        raise ValueError(
            "Training data must contain "
            "both target classes: 0 and 1."
        )

    # IMPORTANT:
    # Sort chronologically to prevent
    # future information entering training.
    dataframe = dataframe.sort_values(
        [
            "match_date",
            "match_id",
        ]
    ).reset_index(
        drop=True
    )

    return dataframe


# ============================================================
# Train V4 Model
# ============================================================

def train_model():

    dataframe = load_dataset()

    # --------------------------------------------------------
    # Chronological 80/20 split
    # --------------------------------------------------------

    split_index = int(
        len(dataframe)
        * (1 - TEST_SIZE)
    )

    train_dataframe = dataframe.iloc[
        :split_index
    ]

    test_dataframe = dataframe.iloc[
        split_index:
    ]

    X_train = train_dataframe[
        FEATURE_COLUMNS
    ]

    y_train = train_dataframe[
        TARGET_COLUMN
    ]

    X_test = test_dataframe[
        FEATURE_COLUMNS
    ]

    y_test = test_dataframe[
        TARGET_COLUMN
    ]

    print(
        "Training Random Forest V4..."
    )

    # --------------------------------------------------------
    # Model
    # --------------------------------------------------------

    model = Pipeline(
        [
            (
                "scaler",
                StandardScaler(),
            ),
            (
                "classifier",
                RandomForestClassifier(
                    n_estimators=N_ESTIMATORS,
                    random_state=RANDOM_STATE,
                    class_weight="balanced",
                    n_jobs=-1,
                ),
            ),
        ]
    )

    # --------------------------------------------------------
    # Fit
    # --------------------------------------------------------

    model.fit(
        X_train,
        y_train,
    )

    # --------------------------------------------------------
    # Predictions
    # --------------------------------------------------------

    predictions = model.predict(
        X_test
    )

    probabilities = (
        model.predict_proba(
            X_test
        )[:, 1]
    )

    # --------------------------------------------------------
    # Metrics
    # --------------------------------------------------------

    accuracy = accuracy_score(
        y_test,
        predictions,
    )

    precision = precision_score(
        y_test,
        predictions,
        zero_division=0,
    )

    recall = recall_score(
        y_test,
        predictions,
        zero_division=0,
    )

    f1 = f1_score(
        y_test,
        predictions,
        zero_division=0,
    )

    roc_auc = roc_auc_score(
        y_test,
        probabilities,
    )

    matrix = confusion_matrix(
        y_test,
        predictions,
    )

    # --------------------------------------------------------
    # Save model
    # --------------------------------------------------------

    MODEL_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    joblib.dump(
        model,
        MODEL_PATH,
    )

    # --------------------------------------------------------
    # Metrics JSON
    # --------------------------------------------------------

    metrics = {
        "model": "RandomForestClassifier-V4",

        "dataset_rows":
            len(dataframe),

        "training_rows":
            len(train_dataframe),

        "test_rows":
            len(test_dataframe),

        "training_start":
            train_dataframe[
                "match_date"
            ].min().strftime(
                "%Y-%m-%d"
            ),

        "training_end":
            train_dataframe[
                "match_date"
            ].max().strftime(
                "%Y-%m-%d"
            ),

        "testing_start":
            test_dataframe[
                "match_date"
            ].min().strftime(
                "%Y-%m-%d"
            ),

        "testing_end":
            test_dataframe[
                "match_date"
            ].max().strftime(
                "%Y-%m-%d"
            ),

        "feature_count":
            len(FEATURE_COLUMNS),

        "features":
            FEATURE_COLUMNS,

        "accuracy":
            round(
                accuracy,
                4,
            ),

        "precision":
            round(
                precision,
                4,
            ),

        "recall":
            round(
                recall,
                4,
            ),

        "f1_score":
            round(
                f1,
                4,
            ),

        "roc_auc":
            round(
                roc_auc,
                4,
            ),

        "confusion_matrix":
            matrix.tolist(),

        "generated_at":
            datetime.now().isoformat(),
    }

    with open(
        METRICS_PATH,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            metrics,
            file,
            indent=4,
        )

    return (
        model,
        metrics,
    )


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":

    print(
        "Starting CricketGPT V4 ML training..."
    )

    model, metrics = train_model()

    print()
    print(
        "Training completed successfully."
    )

    print()
    print(
        "Model saved at:"
    )

    print(
        MODEL_PATH
    )

    print()
    print(
        "Metrics saved at:"
    )

    print(
        METRICS_PATH
    )

    print()
    print(
        "Chronological Evaluation:"
    )

    print(
        f"Training samples: "
        f"{metrics['training_rows']}"
    )

    print(
        f"Test samples: "
        f"{metrics['test_rows']}"
    )

    print(
        f"Training period: "
        f"{metrics['training_start']} "
        f"to "
        f"{metrics['training_end']}"
    )

    print(
        f"Testing period: "
        f"{metrics['testing_start']} "
        f"to "
        f"{metrics['testing_end']}"
    )

    print()
    print(
        "V4 Model Performance:"
    )

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

    print()
    print(
        "Confusion Matrix:"
    )

    print(
        metrics["confusion_matrix"]
    )