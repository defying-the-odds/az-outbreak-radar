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


def lovable_to_ml(form_data: dict) -> dict:
    """
    Translates Lovable frontend form data into Person 1's expected input format.

    Lovable sends:
    {
        "fever": true/false,
        "cough": true/false,
        "shortness_of_breath": true/false,
        "fatigue": true/false,
        "vomiting_diarrhea": true/false,
        "rash": true/false,
        "body_aches": true/false,
        "recent_travel": true/false,
        "travel_destination": "Mexico" or null,
        "animal_exposure": true/false,
        "mosquito_bites": true/false,
        "zip_code": "85719",
        "age_range": "18-24",
        "pre_existing": ["none"]
    }

    Person 1 expects:
    {
        "fever": 0/1,
        "cough": 0/1,
        "travel": 0/1,
        "animal_exposure": 0/1,
        "mosquito_index": float (0.0 to 1.0)
    }
    """
    return {
        "fever": int(bool(form_data.get("fever", False))),
        "cough": int(bool(form_data.get("cough", False))),
        "travel": int(bool(form_data.get("recent_travel", False))),
        "animal_exposure": int(bool(form_data.get("animal_exposure", False))),
        # convert mosquito_bites boolean to a float index
        # if they got bitten, treat as 0.7 risk; otherwise 0.1
        "mosquito_index": 0.7 if form_data.get("mosquito_bites", False) else 0.1,
    }


def enrich_ml_result(ml_result: dict, form_data: dict) -> dict:
    """
    Takes Person 1's ML output and adds extra info from
    form fields that Person 1 doesn't handle (zip_code, age, etc.)

    This makes the output richer for the Lovable frontend.
    """
    result = dict(ml_result)

    # add extra drivers based on fields Person 1 doesn't process
    extra_drivers = []

    if form_data.get("shortness_of_breath"):
        extra_drivers.append("shortness of breath")
        result["score"] = min(1.0, result["score"] + 0.1)

    if form_data.get("vomiting_diarrhea"):
        extra_drivers.append("vomiting/diarrhea")
        result["score"] = min(1.0, result["score"] + 0.08)

    if form_data.get("rash"):
        extra_drivers.append("rash")
        result["score"] = min(1.0, result["score"] + 0.05)

    if form_data.get("fatigue"):
        extra_drivers.append("fatigue")
        result["score"] = min(1.0, result["score"] + 0.03)

    if form_data.get("body_aches"):
        extra_drivers.append("body aches")
        result["score"] = min(1.0, result["score"] + 0.03)

    if "immunocompromised" in form_data.get("pre_existing", []):
        extra_drivers.append("immunocompromised status")
        result["score"] = min(1.0, result["score"] + 0.1)

    if extra_drivers:
        result["drivers"] = result.get("drivers", []) + extra_drivers

    # recalculate category after adjustments
    score = result["score"]
    if score >= 0.65:
        result["category"] = "High"
    elif score >= 0.35:
        result["category"] = "Moderate"
    else:
        result["category"] = "Low"

    # convert score to 0-100 scale for the Lovable gauge display
    result["score_display"] = round(score * 100)

    # add travel destination if provided
    if form_data.get("travel_destination"):
        result["travel_destination"] = form_data["travel_destination"]

    # add zip code for reference
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

    # translate lovable format → person 1's format
    ml_input = lovable_to_ml(form_data)

    # run person 1's risk engine
    ml_result = get_risk_score(ml_input)

    # enrich with extra symptoms person 1 doesn't handle
    enriched = enrich_ml_result(ml_result, form_data)

    return jsonify(enriched)


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
