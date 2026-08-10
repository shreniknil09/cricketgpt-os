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

from app.ml.config import (
    FEATURE_COLUMNS,
    TARGET_COLUMN,
    MODEL_PATH,
    METRICS_PATH,
    N_ESTIMATORS,
    TRAINING_DATA_PATH,
)


def load_dataset():

    if not TRAINING_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Training dataset not found: "
            f"{TRAINING_DATA_PATH}"
        )

    dataframe = pd.read_csv(
        TRAINING_DATA_PATH
    )

    required_columns = (
        ["match_date"]
        + FEATURE_COLUMNS
        + [TARGET_COLUMN]
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

    dataframe["match_date"] = pd.to_datetime(
        dataframe["match_date"],
        errors="coerce",
    )

    dataframe = dataframe.dropna(
        subset=[
            "match_date",
            TARGET_COLUMN,
            *FEATURE_COLUMNS,
        ]
    )

    if len(dataframe) < 20:
        raise ValueError(
            "At least 20 valid matches "
            "are required for training."
        )

    if dataframe[TARGET_COLUMN].nunique() < 2:
        raise ValueError(
            "Training data must contain "
            "both target classes: 0 and 1."
        )

    dataframe = dataframe.sort_values(
        by=[
            "match_date",
            "match_id",
        ]
    ).reset_index(drop=True)

    return dataframe


def train_model():

    dataframe = load_dataset()

    # ---------------------------------
    # Chronological split
    # ---------------------------------

    split_index = int(
        len(dataframe) * 0.80
    )

    if split_index <= 0:
        raise ValueError(
            "Not enough data for training."
        )

    if split_index >= len(dataframe):
        raise ValueError(
            "Not enough data for testing."
        )

    train_data = dataframe.iloc[
        :split_index
    ]

    test_data = dataframe.iloc[
        split_index:
    ]

    X_train = train_data[
        FEATURE_COLUMNS
    ]

    y_train = train_data[
        TARGET_COLUMN
    ]

    X_test = test_data[
        FEATURE_COLUMNS
    ]

    y_test = test_data[
        TARGET_COLUMN
    ]

    if y_train.nunique() < 2:
        raise ValueError(
            "Training portion contains "
            "only one target class."
        )

    if y_test.nunique() < 2:
        raise ValueError(
            "Testing portion contains "
            "only one target class."
        )

    # ---------------------------------
    # Model
    # ---------------------------------

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
                    random_state=42,
                    class_weight="balanced",
                    n_jobs=-1,
                ),
            ),
        ]
    )

    print(
        "Training Random Forest..."
    )

    model.fit(
        X_train,
        y_train,
    )

    # ---------------------------------
    # Predictions
    # ---------------------------------

    y_pred = model.predict(
        X_test
    )

    y_probability = model.predict_proba(
        X_test
    )[:, 1]

    # ---------------------------------
    # Evaluation
    # ---------------------------------

    accuracy = accuracy_score(
        y_test,
        y_pred,
    )

    precision = precision_score(
        y_test,
        y_pred,
        zero_division=0,
    )

    recall = recall_score(
        y_test,
        y_pred,
        zero_division=0,
    )

    f1 = f1_score(
        y_test,
        y_pred,
        zero_division=0,
    )

    roc_auc = roc_auc_score(
        y_test,
        y_probability,
    )

    matrix = confusion_matrix(
        y_test,
        y_pred,
    )

    # ---------------------------------
    # Save model
    # ---------------------------------

    MODEL_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    joblib.dump(
        model,
        MODEL_PATH,
    )

    # ---------------------------------
    # Save metrics
    # ---------------------------------

    metrics = {

        "model":
            "RandomForestClassifier",

        "dataset_rows":
            int(len(dataframe)),

        "training_rows":
            int(len(train_data)),

        "test_rows":
            int(len(test_data)),

        "training_start":
            str(
                train_data[
                    "match_date"
                ].min().date()
            ),

        "training_end":
            str(
                train_data[
                    "match_date"
                ].max().date()
            ),

        "testing_start":
            str(
                test_data[
                    "match_date"
                ].min().date()
            ),

        "testing_end":
            str(
                test_data[
                    "match_date"
                ].max().date()
            ),

        "feature_count":
            len(FEATURE_COLUMNS),

        "features":
            FEATURE_COLUMNS,

        "accuracy":
            round(
                float(accuracy),
                4,
            ),

        "precision":
            round(
                float(precision),
                4,
            ),

        "recall":
            round(
                float(recall),
                4,
            ),

        "f1_score":
            round(
                float(f1),
                4,
            ),

        "roc_auc":
            round(
                float(roc_auc),
                4,
            ),

        "confusion_matrix":
            matrix.tolist(),
    }

    METRICS_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with METRICS_PATH.open(
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


if __name__ == "__main__":

    print(
        "Starting CricketGPT ML training..."
    )

    model, metrics = train_model()

    print(
        "\nTraining completed successfully."
    )

    print(
        "\nModel saved at:"
    )

    print(
        MODEL_PATH
    )

    print(
        "\nMetrics saved at:"
    )

    print(
        METRICS_PATH
    )

    print(
        "\nChronological Evaluation:"
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

    print(
        "\nModel Performance:"
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

    print(
        "\nConfusion Matrix:"
    )

    print(
        metrics["confusion_matrix"]
    )