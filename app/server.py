"""
Flask API Server — Connects the Lovable frontend to the Python backend.

Bridges the gap between:
  - Lovable form data format (booleans, multiple symptoms)
  - Person 1's ML input format (0/1 integers, mosquito_index float)
  - Person 3's analytics output format (community score, hotspots, trends)

Run with: python app/server.py
"""

import sys
import os

# add project root to path so imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify
from flask_cors import CORS

from ml.risk_engine import get_risk_score
from analytics.community import (
    generate_mock_population,
    compute_community_risk,
    region_hotspots,
    generate_explanation,
    recommend_action,
    get_report,
)

app = Flask(__name__)
CORS(app)  # allows Lovable frontend to call this API


# ---- HELPERS ----

# CDC high risk travel destinations
HIGH_RISK_DESTINATIONS = [
    "mexico",
    "india",
    "china",
    "brazil",
    "indonesia",
    "nigeria",
    "ethiopia",
    "congo",
    "pakistan",
    "bangladesh",
]


def lovable_to_ml(form_data: dict) -> dict:
    """
    Translates Lovable frontend form data into Person 1's updated ML format.
    Person 1 (Aswin) now handles ALL symptoms, pre-existing conditions,
    age multipliers, and has a trained logistic regression model.
    """
    pre_existing = form_data.get("pre_existing", [])
    destination = form_data.get("travel_destination", "")

    return {
        # symptoms
        "fever": int(bool(form_data.get("fever", False))),
        "cough": int(bool(form_data.get("cough", False))),
        "shortness_of_breath": int(bool(form_data.get("shortness_of_breath", False))),
        "fatigue": int(bool(form_data.get("fatigue", False))),
        "vomiting_diarrhea": int(bool(form_data.get("vomiting_diarrhea", False))),
        "rash": int(bool(form_data.get("rash", False))),
        "body_aches": int(bool(form_data.get("body_aches", False))),
        # context
        "travel": int(bool(form_data.get("recent_travel", False))),
        "animal_exposure": int(bool(form_data.get("animal_exposure", False))),
        "mosquito_index": 0.7 if form_data.get("mosquito_bites", False) else 0.1,
        "mosquito_bite": int(bool(form_data.get("mosquito_bites", False))),
        # pre-existing conditions
        "diabetes": int("diabetes" in [p.lower() for p in pre_existing]),
        "asthma": int("asthma" in [p.lower() for p in pre_existing]),
        "immunocompromised": int(
            "immunocompromised" in [p.lower() for p in pre_existing]
        ),
        # age and location
        "age_range": form_data.get("age_range", None),
        "location": form_data.get("zip_code", "unknown"),
        # travel risk from CDC advisories
        "travel_risk": (
            0.2
            if destination and destination.lower() in HIGH_RISK_DESTINATIONS
            else (0.1 if destination else 0.0)
        ),
    }


def format_for_lovable(ml_result: dict, form_data: dict) -> dict:
    """
    Formats Person 1's ML output for the Lovable frontend.
    No extra scoring — Aswin's engine + ML model handles everything now.
    """
    result = dict(ml_result)

    # convert 0-1 score to 0-100 for the gauge display
    result["score_display"] = round(result["score"] * 100)

    # pass through travel destination and zip code
    if form_data.get("travel_destination"):
        result["travel_destination"] = form_data["travel_destination"]
    if form_data.get("zip_code"):
        result["zip_code"] = form_data["zip_code"]

    return result


# ---- API ENDPOINTS ----


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "AZ Outbreak Radar API is running"})


@app.route("/api/assess", methods=["POST"])
def assess_risk():
    """
    Accepts symptom data from the Lovable form,
    translates it for Person 1's ML engine,
    enriches the result, and returns it.
    """
    form_data = request.get_json()

    if not form_data:
        return jsonify({"error": "No data provided"}), 400

    # translate lovable booleans → person 1's 0/1 format
    ml_input = lovable_to_ml(form_data)

    # run Aswin's risk engine (ML model + rule-based fallback)
    ml_result = get_risk_score(ml_input)

    # format for lovable frontend display
    formatted = format_for_lovable(ml_result, form_data)

    return jsonify(formatted)


@app.route("/api/community", methods=["GET"])
def community():
    """
    Runs Person 3's analytics and returns the community dashboard data.
    Uses the exact format from Person 3's get_report() function.
    """
    # generate mock population data
    population = generate_mock_population(200)

    # compute metrics
    today_avg = compute_community_risk(population)
    yesterday_avg = today_avg - 0.03  # simulated baseline

    # get hotspots
    hotspots = region_hotspots(population)

    # generate insight
    insight = generate_explanation(today_avg, hotspots)

    # return in Person 3's exact format
    report = get_report(today_avg, yesterday_avg, hotspots, insight)

    return jsonify(report)


@app.route("/api/trends", methods=["GET"])
def trends():
    """
    Returns daily trend data for the Lovable chart.
    Uses mock data for the hackathon demo.
    """
    import random

    random.seed(42)

    # generate 14 days of trend data
    from datetime import datetime, timedelta

    base = datetime.now()

    daily = []
    count = 15  # start value
    for i in range(13, -1, -1):
        date = (base - timedelta(days=i)).strftime("%b %d")
        count = max(5, count + random.randint(-3, 8))
        daily.append({"date": date, "count": count})

    return jsonify({"daily_counts": daily})


# ---- MAIN ----

if __name__ == "__main__":
    print("\n=== AZ Outbreak Radar API ===")
    print("Running on http://localhost:5000")
    print()
    print("Endpoints:")
    print("  POST /api/assess     → submit symptoms, get risk score")
    print("  GET  /api/community  → community dashboard data")
    print("  GET  /api/trends     → daily trend chart data")
    print("  GET  /api/health     → health check")
    print()
    print("Lovable frontend should call these endpoints.")
    print("================================\n")
    app.run(debug=True, port=8000)
