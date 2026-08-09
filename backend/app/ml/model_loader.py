import joblib


from app.ml.config import (
    MODEL_PATH,
)


_model = None


def load_model():
    global _model

    if _model is not None:
        return _model

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "Trained ML model not found. "
            "Train the model first."
        )

    _model = joblib.load(
        MODEL_PATH
    )

    return _model


def clear_model_cache():
    global _model

    _model = None