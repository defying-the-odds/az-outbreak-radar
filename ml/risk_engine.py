# ml/risk_engine.py

import pickle
import os
import numpy as np
from ml.features import extract_features, get_risk_drivers
from ml.model import weighted_risk_score, get_category, get_explanation, get_age_multiplier

FEATURE_ORDER = [
    "fever",
    "cough",
    "travel",
    "animal_exposure",
    "mosquito_index",
    "shortness_of_breath",
    "fatigue",
    "vomiting_diarrhea",
    "rash",
    "body_aches",
    "mosquito_bite",
    "diabetes",
    "asthma",
    "immunocompromised"
]


def load_ml_model():
    """
    Loads the trained logistic regression model.
    Returns None if model hasn't been trained yet.
    """
    model_path = "ml/saved/model.pkl"
    if not os.path.exists(model_path):
        return None
    with open(model_path, "rb") as f:
        return pickle.load(f)


def get_ml_score(features: dict) -> float:
    """
    Uses trained ML model to predict risk score.
    Falls back to rule based scoring if model not found.
    """
    model = load_ml_model()
    if not model:
        return None

    # Build feature vector in correct order
    feature_vector = np.array([
        features.get(f, 0) for f in FEATURE_ORDER
    ]).reshape(1, -1)

    # Get probability of high risk
    prob = model.predict_proba(feature_vector)[0][1]
    return round(float(prob), 2)


def get_risk_score(input_data: dict) -> dict:
    """
    MAIN FUNCTION — this is what the backend calls.
    Uses ML model if available, falls back to rule based scoring.
    """

    # Step 1 — clean the input
    features = extract_features(input_data)

    # Step 2 — get rule based score
    rule_score = weighted_risk_score(features)

    # Step 3 — get ML score
    ml_score = get_ml_score(features)

    # Step 4 — decide final score
    if ml_score is not None:
        # ML model is available — use it
        final_score = ml_score
        print(f"\nRule Based Score:  {rule_score}")
        print(f"ML Model Score:    {ml_score}")
        print(f"Final Score:       {final_score} ← ML wins")
    else:
        # No ML model yet — fall back to rules
        final_score = rule_score
        print("ML model not found, using rule based scoring.")

    # Apply age multiplier
    age_range = features.get("age_range", None)
    if age_range:
        multiplier = get_age_multiplier(age_range)
        final_score = round(min(1.0, max(0.0, final_score * multiplier)), 2)

    # Step 5 — get category
    category = get_category(final_score)

    # Step 6 — get drivers
    drivers = get_risk_drivers(features, final_score)

    # Step 7 — get explanation
    explanation = get_explanation(category, drivers)

    return {
        "score": final_score,
        "category": category,
        "drivers": drivers,
        "explanation": explanation
    }