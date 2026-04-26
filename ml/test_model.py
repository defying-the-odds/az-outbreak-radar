# ml/test_model.py

from ml.risk_engine import get_risk_score

# Test 1 — High risk
result = get_risk_score({
    "fever": 1,
    "cough": 1,
    "travel": 1,
    "animal_exposure": 0,
    "mosquito_index": 0.8
})
print("HIGH RISK TEST:", result)

# Test 2 — Low risk
result = get_risk_score({
    "fever": 0,
    "cough": 0,
    "travel": 0,
    "animal_exposure": 0,
    "mosquito_index": 0.1
})
print("LOW RISK TEST:", result)

# Test 3 — Moderate risk
result = get_risk_score({
    "fever": 0,
    "cough": 1,
    "travel": 1,
    "animal_exposure": 0,
    "mosquito_index": 0.3
})
print("MODERATE RISK TEST:", result)