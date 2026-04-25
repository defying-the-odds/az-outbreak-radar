# az-outbreak-radar
hackathon 2026 Project

📘 AZ Outbreak Radar — Team Setup Guide
🧠 Project Overview

We are building an AI-powered early outbreak detection system for Arizona that:

Collects self-reported symptoms
Uses ML + rules to estimate individual risk
Aggregates data into community-level outbreak signals
Displays insights through a Streamlit dashboard
📁 Project Structure
az-outbreak-radar/
│
├── app/                  # Streamlit frontend (User interface)
│   └── app.py
│
├── ml/                   # Machine learning + risk engine
│   ├── model.py
│   ├── risk_engine.py
│   ├── features.py
│
├── analytics/            # Community + trend analysis
│   ├── community.py
│   ├── trends.py
│   ├── hotspot.py
│
├── data/                 # Mock/synthetic data
│   ├── mock_users.py
│   ├── sample_inputs.json
│
├── assets/
│   ├── diagrams/
│   ├── screenshots/
│
├── requirements.txt
└── README.md
🧑‍💻 Team Roles & Responsibilities
🧑‍💻 Person 1 — ML + Risk Engine

Folder: /ml

Responsibilities:
Train logistic regression model
Build risk scoring system
Convert user inputs → feature vectors
Key files:
model.py → ML training
risk_engine.py → combines ML + rules
features.py → feature engineering
🧑‍💻 Person 2 — Streamlit App (Frontend)

Folder: /app

Responsibilities:
Build user interface
Input form for symptoms + travel
Display results (risk score + explanation)
Connect ML + analytics outputs
Key file:
app.py → MAIN APPLICATION
🧑‍💻 Person 3 — Analytics + Community Intelligence

Folder: /analytics

Responsibilities:
Aggregate multiple users
Compute community risk trends
Detect hotspots
Generate insights for dashboard
Key files:
community.py → aggregation logic
trends.py → time-based analysis
hotspot.py → region-based risk detection
⚙️ Setup Instructions (DO THIS FIRST)
1. Clone repo
git clone https://github.com/YOUR_USERNAME/az-outbreak-radar.git
cd az-outbreak-radar
2. Open in VS Code
code .
3. Create virtual environment
Mac/Linux:
python3 -m venv venv
source venv/bin/activate
Windows:
python -m venv venv
venv\Scripts\activate
4. Install dependencies
pip install -r requirements.txt
5. Run the app
streamlit run app/app.py
📦 Data Flow (IMPORTANT)
User Input
   ↓
ML Risk Engine (ml/)
   ↓
Individual Risk Score
   ↓
Analytics Layer (analytics/)
   ↓
Community Dashboard Output
🧠 Shared Data Contract (DO NOT CHANGE WITHOUT TEAM)
Input format:
{
  "fever": 0/1,
  "cough": 0/1,
  "travel": 0/1,
  "animal_exposure": 0/1,
  "mosquito_index": float,
  "location": str
}
Output format:
{
  "score": float,
  "category": "Low | Moderate | High",
  "drivers": [list],
  "explanation": str
}
🚀 Work Rules (VERY IMPORTANT)
✔ Parallel work is required
Everyone codes at the same time
No waiting for others
✔ Each folder is independent
Do NOT edit other folders unless integration phase
✔ Use fake data first
UI and analytics should work before full ML integration
🔥 Development Phases
Phase 1 (NOW)
Everyone builds their module independently
Phase 2
Connect ML → UI
Phase 3
Connect analytics → dashboard
Phase 4
Polish + demo + slides
🏆 Final Goal

A working system that:

Accepts user symptom reports
Outputs individual risk
Shows community outbreak trends
Explains WHY risk is high/low
