# ml/risk_engine.py

from ml.features import extract_features, get_risk_drivers
from ml.model import weighted_risk_score, get_category, get_explanation


def get_risk_score(input_data: dict) -> dict:
    # Step 1 — clean the input
    features = extract_features(input_data)

    # Step 2 — calculate score
    score = weighted_risk_score(features)

    # Step 3 — get category
    category = get_category(score)

    # Step 4 — get drivers
    drivers = get_risk_drivers(features, score)

    # Step 5 — get explanation
    explanation = get_explanation(category, drivers)

    return {
        "score": score,
        "category": category,
        "drivers": drivers,
        "explanation": explanation
    }