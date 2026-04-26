# ml/features.py

def extract_features(input_data: dict) -> dict:
    return {
        "fever": int(input_data.get("fever", 0)),
        "cough": int(input_data.get("cough", 0)),
        "travel": int(input_data.get("travel", 0)),
        "animal_exposure": int(input_data.get("animal_exposure", 0)),
        "mosquito_index": float(input_data.get("mosquito_index", 0.0))
    }


def get_risk_drivers(features: dict, score: float) -> list:
    drivers = []

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

    return drivers