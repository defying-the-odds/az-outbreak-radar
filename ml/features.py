# ml/features.py

def extract_features(input_data: dict) -> dict:
    return {
        # Original symptoms
        "fever": int(input_data.get("fever", 0)),
        "cough": int(input_data.get("cough", 0)),
        "travel": int(input_data.get("travel", 0)),
        "animal_exposure": int(input_data.get("animal_exposure", 0)),
        "mosquito_index": float(input_data.get("mosquito_index", 0.0)),

        # New symptoms
        "shortness_of_breath": int(input_data.get("shortness_of_breath", 0)),
        "fatigue": int(input_data.get("fatigue", 0)),
        "vomiting_diarrhea": int(input_data.get("vomiting_diarrhea", 0)),
        "rash": int(input_data.get("rash", 0)),
        "body_aches": int(input_data.get("body_aches", 0)),
        "mosquito_bite": int(input_data.get("mosquito_bite", 0)),

        # Pre existing conditions
        "diabetes": int(input_data.get("diabetes", 0)),
        "asthma": int(input_data.get("asthma", 0)),
        "immunocompromised": int(input_data.get("immunocompromised", 0)),

        # Context
        "age_range": input_data.get("age_range", None),
        "location": input_data.get("location", "unknown")
    }


def get_risk_drivers(features: dict, score: float) -> list:
    drivers = []

    # Original symptoms
    if features["fever"] == 1:
        drivers.append("fever")
    if features["cough"] == 1:
        drivers.append("cough")
    if features["travel"] == 1:
        drivers.append("recent travel")
    if features["animal_exposure"] == 1:
        drivers.append("animal exposure")
    if features["mosquito_index"] > 0.5:
        drivers.append("high mosquito activity")

    # New symptoms
    if features["shortness_of_breath"] == 1:
        drivers.append("shortness of breath")
    if features["fatigue"] == 1:
        drivers.append("fatigue")
    if features["vomiting_diarrhea"] == 1:
        drivers.append("vomiting or diarrhea")
    if features["rash"] == 1:
        drivers.append("rash")
    if features["body_aches"] == 1:
        drivers.append("body aches")
    if features["mosquito_bite"] == 1:
        drivers.append("recent mosquito bite")

    # Pre existing conditions
    if features["diabetes"] == 1:
        drivers.append("diabetes")
    if features["asthma"] == 1:
        drivers.append("asthma")
    if features["immunocompromised"] == 1:
        drivers.append("immunocompromised")

    return drivers