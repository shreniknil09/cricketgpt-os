import json

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
)


from app.ml.config import (
    METRICS_PATH,
)


def evaluate_model(
    model,
    X_test,
    y_test,
):
    """
    Evaluate the trained classification model.
    """

    predictions = model.predict(
        X_test
    )

    probabilities = (
        model.predict_proba(
            X_test
        )[:, 1]
    )

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

    try:
        roc_auc = roc_auc_score(
            y_test,
            probabilities,
        )

    except ValueError:
        roc_auc = 0.0

    matrix = confusion_matrix(
        y_test,
        predictions,
    )

    metrics = {
        "accuracy": round(
            float(accuracy),
            4,
        ),

        "precision": round(
            float(precision),
            4,
        ),

        "recall": round(
            float(recall),
            4,
        ),

        "f1_score": round(
            float(f1),
            4,
        ),

        "roc_auc": round(
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

    return metrics