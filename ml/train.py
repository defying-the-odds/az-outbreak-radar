# ml/train.py

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle
import os

def generate_training_data(n_samples=1000):
    """
    Generates synthetic training data based on CDC outbreak patterns.
    """
    np.random.seed(42)

    # Generate random symptom combinations
    data = {
        "fever":                np.random.randint(0, 2, n_samples),
        "cough":                np.random.randint(0, 2, n_samples),
        "travel":               np.random.randint(0, 2, n_samples),
        "animal_exposure":      np.random.randint(0, 2, n_samples),
        "mosquito_index":       np.random.uniform(0, 1, n_samples),
        "shortness_of_breath":  np.random.randint(0, 2, n_samples),
        "fatigue":              np.random.randint(0, 2, n_samples),
        "vomiting_diarrhea":    np.random.randint(0, 2, n_samples),
        "rash":                 np.random.randint(0, 2, n_samples),
        "body_aches":           np.random.randint(0, 2, n_samples),
        "mosquito_bite":        np.random.randint(0, 2, n_samples),
        "diabetes":             np.random.randint(0, 2, n_samples),
        "asthma":               np.random.randint(0, 2, n_samples),
        "immunocompromised":    np.random.randint(0, 2, n_samples),
    }

    # Build feature matrix
    X = np.column_stack(list(data.values()))

    # Generate labels based on CDC risk weights
    raw_score = (
        data["fever"] * 0.4 +
        data["cough"] * 0.2 +
        data["travel"] * 0.2 +
        data["animal_exposure"] * 0.1 +
        data["mosquito_index"] * 0.1 +
        data["shortness_of_breath"] * 0.3 +
        data["fatigue"] * 0.15 +
        data["vomiting_diarrhea"] * 0.15 +
        data["rash"] * 0.1 +
        data["body_aches"] * 0.1 +
        data["mosquito_bite"] * 0.1 +
        data["diabetes"] * 0.15 +
        data["asthma"] * 0.1 +
        data["immunocompromised"] * 0.2
    )

    # Label as high risk (1) or low risk (0)
    y = (raw_score >= 0.5).astype(int)

    return X, y


def train_model():
    print("Generating 1000 CDC based training samples...")
    X, y = generate_training_data(1000)

    # Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("Training Logistic Regression model...")
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    # Check accuracy
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {round(accuracy * 100, 2)}%")

    # Save the model
    os.makedirs("ml/saved", exist_ok=True)
    with open("ml/saved/model.pkl", "wb") as f:
        pickle.dump(model, f)

    print("Model saved successfully to ml/saved/model.pkl!")
    return model


if __name__ == "__main__":
    train_model()