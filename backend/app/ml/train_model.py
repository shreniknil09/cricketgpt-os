from pathlib import Path

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


from app.ml.config import (
    FEATURE_COLUMNS,
    TARGET_COLUMN,
    MODEL_PATH,
    TEST_SIZE,
    RANDOM_STATE,
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
        FEATURE_COLUMNS
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

    dataframe = dataframe[
        required_columns
    ].dropna()

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

    return dataframe


def train_model():
    dataframe = load_dataset()

    X = dataframe[
        FEATURE_COLUMNS
    ]

    y = dataframe[
        TARGET_COLUMN
    ]

    X_train, X_test, y_train, y_test = (
        train_test_split(
            X,
            y,
            test_size=TEST_SIZE,
            random_state=RANDOM_STATE,
            stratify=y,
        )
    )

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

    model.fit(
        X_train,
        y_train,
    )

    MODEL_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    joblib.dump(
        model,
        MODEL_PATH,
    )

    return (
        model,
        X_test,
        y_test,
    )


if __name__ == "__main__":

    print(
        "Starting CricketGPT ML training..."
    )

    model, X_test, y_test = train_model()

    print(
        f"Training completed successfully."
    )

    print(
        f"Model saved at:"
    )

    print(
        MODEL_PATH
    )

    print(
        f"Test samples: {len(X_test)}"
    )