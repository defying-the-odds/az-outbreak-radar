# ml/visualize.py

import pickle
import numpy as np
import os

FEATURE_NAMES = [
    "Fever",
    "Cough",
    "Travel",
    "Animal Exposure",
    "Mosquito Index",
    "Shortness of Breath",
    "Fatigue",
    "Vomiting/Diarrhea",
    "Rash",
    "Body Aches",
    "Mosquito Bite",
    "Diabetes",
    "Asthma",
    "Immunocompromised"
]


def load_model():
    model_path = "ml/saved/model.pkl"
    if not os.path.exists(model_path):
        print("Model not found! Run train.py first.")
        return None
    with open(model_path, "rb") as f:
        return pickle.load(f)


def show_feature_importance():
    model = load_model()
    if not model:
        return

    # Get coefficients from logistic regression
    coefficients = model.coef_[0]
    importance = np.abs(coefficients)
    importance_pct = (importance / importance.sum()) * 100

    print("\n" + "="*45)
    print("       FEATURE IMPORTANCE CHART")
    print("="*45)

    # Sort by importance
    sorted_idx = np.argsort(importance_pct)[::-1]

    for idx in sorted_idx:
        name = FEATURE_NAMES[idx]
        pct = importance_pct[idx]
        bar = "█" * int(pct / 2)
        print(f"{name:<22} {bar:<20} {pct:.1f}%")

    print("="*45)


def compare_scores(input_data: dict, ml_score: float, rule_score: float):
    print("\n" + "="*45)
    print("        SCORING COMPARISON")
    print("="*45)
    print(f"Rule Based Score:   {rule_score}")
    print(f"ML Model Score:     {ml_score}")
    print(f"Final Score:        {ml_score}  ← ML wins")
    print("="*45)


if __name__ == "__main__":
    show_feature_importance()