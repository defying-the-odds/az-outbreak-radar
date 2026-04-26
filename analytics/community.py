import random

# =========================
# CONFIG
# =========================

REGIONS = ["Tucson", "Phoenix", "Tempe", "Flagstaff"]


# =========================
# DATA GENERATION
# =========================

def generate_mock_population(n=100):
    """
    Simulates population-level risk data.
    Each entry = {score, region}
    """
    return [
        {
            "score": random.uniform(0, 1),
            "region": random.choice(REGIONS)
        }
        for _ in range(n)
    ]


# =========================
# CORE METRICS
# =========================

def compute_community_risk(population):
    scores = [p["score"] for p in population]
    return sum(scores) / len(scores)


def detect_trend(today, yesterday):
    diff = today - yesterday

    if diff > 0.05:
        return "Rising ⚠️"
    elif diff < -0.05:
        return "Falling 📉"
    else:
        return "Stable ✅"


# =========================
# REGION ANALYSIS
# =========================

def region_hotspots(population):
    """
    Counts high-risk individuals per region.
    """
    hotspots = {}

    for p in population:
        if p["score"] > 0.7:
            region = p["region"]
            hotspots[region] = hotspots.get(region, 0) + 1

    return hotspots


def classify_region_risk(count):
    if count >= 10:
        return "HIGH 🔴"
    elif count >= 5:
        return "MODERATE 🟡"
    else:
        return "LOW 🟢"


# =========================
# INSIGHT ENGINE
# =========================

def generate_explanation(avg, hotspots):
    regions = list(hotspots.keys())

    if avg > 0.6 and regions:
        return f"Elevated risk detected in {', '.join(regions)} with emerging cluster patterns."

    if avg > 0.6:
        return "Elevated symptom reporting across community."

    if len(hotspots) >= 2:
        return "Multiple regional clusters emerging."

    return "No significant outbreak signals detected."


def recommend_action(avg):
    if avg > 0.7:
        return "ALERT: Immediate public health monitoring recommended"
    elif avg > 0.5:
        return "WATCH: Increased surveillance suggested"
    else:
        return "NORMAL: No action required"


# =========================
# OUTPUT (CONSOLE VERSION)
# =========================

def print_report(today_avg, yesterday_avg, hotspots, insight):
    print("\n========================")
    print(" AZ OUTBREAK RADAR REPORT ")
    print("========================\n")

    print(f"Community Risk Score: {round(today_avg, 3)}")
    print(f"Trend: {detect_trend(today_avg, yesterday_avg)}")

    print("\nRegional Hotspots:")
    if hotspots:
        for region, count in hotspots.items():
            level = classify_region_risk(count)
            print(f" - {region}: {count} ({level})")
    else:
        print(" - None detected")

    print(f"\nInsight:\n{insight}")

    print(f"\nRecommended Action:\n{recommend_action(today_avg)}")

    print("\n========================\n")


# =========================
# INTEGRATION-READY OUTPUT
# =========================

def get_report(today_avg, yesterday_avg, hotspots, insight):
    """
    Clean return format for Streamlit/UI integration.
    """
    return {
        "community_score": today_avg,
        "trend": detect_trend(today_avg, yesterday_avg),
        "hotspots": {
            region: {
                "count": count,
                "level": classify_region_risk(count)
            }
            for region, count in hotspots.items()
        },
        "insight": insight,
        "action": recommend_action(today_avg)
    }


# =========================
# DEMO RUN
# =========================

if __name__ == "__main__":
    population = generate_mock_population(100)

    today_avg = compute_community_risk(population)

    # simulated baseline
    yesterday_avg = today_avg - random.uniform(-0.05, 0.05)

    hotspots = region_hotspots(population)
    insight = generate_explanation(today_avg, hotspots)

    print_report(today_avg, yesterday_avg, hotspots, insight)