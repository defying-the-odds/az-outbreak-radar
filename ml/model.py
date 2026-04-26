# ml/model.py

def weighted_risk_score(features: dict) -> float:
    score = (
        features["fever"] * 0.4 +
        features["cough"] * 0.3 +
        features["travel"] * 0.2 +
        features["animal_exposure"] * 0.1 +
        features["mosquito_index"] * 0.2
    )
    return round(min(1.0, max(0.0, score)), 2)


def get_category(score: float) -> str:
    if score >= 0.65:
        return "High"
    elif score >= 0.35:
        return "Moderate"
    else:
        return "Low"


def get_explanation(category: str, drivers: list) -> str:
    if not drivers:
        return "No significant risk factors detected. Continue monitoring."

    driver_text = ", ".join(drivers)

    if category == "High":
        return f"High risk detected due to: {driver_text}. Seek medical advice and avoid crowded areas."
    elif category == "Moderate":
        return f"Moderate risk detected due to: {driver_text}. Monitor symptoms closely."
    else:
        return f"Low risk. Minor indicators present: {driver_text}."