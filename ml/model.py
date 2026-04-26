# ml/model.py

def get_age_multiplier(age_range: str) -> float:
    """
    Age risk multipliers based on CDC published data.
    https://www.cdc.gov/coronavirus/2019-ncov/need-extra-precautions/people-with-medical-conditions.html
    """
    age_multipliers = {
        "0-17":  1.1,
        "18-34": 1.0,
        "35-54": 1.1,
        "55-64": 1.3,
        "65+":   1.5
    }
    return age_multipliers.get(age_range, 1.0)


def weighted_risk_score(features: dict) -> float:
    score = (
        # Original symptoms
        features.get("fever", 0) * 0.4 +
        features.get("cough", 0) * 0.2 +
        features.get("travel", 0) * 0.2 +
        features.get("animal_exposure", 0) * 0.1 +
        features.get("mosquito_index", 0.0) * 0.1 +

        # New symptoms
        features.get("shortness_of_breath", 0) * 0.3 +
        features.get("fatigue", 0) * 0.15 +
        features.get("vomiting_diarrhea", 0) * 0.15 +
        features.get("rash", 0) * 0.1 +
        features.get("body_aches", 0) * 0.1 +
        features.get("mosquito_bite", 0) * 0.1 +

        # Pre existing conditions
        features.get("diabetes", 0) * 0.15 +
        features.get("asthma", 0) * 0.1 +
        features.get("immunocompromised", 0) * 0.2 +

        # Travel destination risk from CDC advisories
        features.get("travel_risk", 0.0)
    )

    # Apply age multiplier from CDC data
    age_range = features.get("age_range", None)
    if age_range:
        multiplier = get_age_multiplier(age_range)
        score = score * multiplier

    # Clamp between 0 and 1
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