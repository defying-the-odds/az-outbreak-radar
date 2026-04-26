# backend/services/aggregator.py

def aggregate_community_risk(reports: list) -> dict:
    
    # If no reports, return default
    if not reports:
        return {
            "community_risk_score": 0.0,
            "total_reports": 0,
            "trend": "stable"
        }

    # Calculate average risk score across all reports
    total_score = sum(r["score"] for r in reports)
    avg_score = round(total_score / len(reports), 2)

    # Determine trend
    if avg_score >= 0.65:
        trend = "increasing"
    elif avg_score >= 0.35:
        trend = "stable"
    else:
        trend = "decreasing"

    return {
        "community_risk_score": avg_score,
        "total_reports": len(reports),
        "trend": trend
    }


def aggregate_by_region(reports: list) -> list:
    
    # Group reports by location
    regions = {}

    for report in reports:
        location = report.get("location", "unknown")
        if location not in regions:
            regions[location] = []
        regions[location].append(report["score"])

    # Calculate average per region
    result = []
    for region, scores in regions.items():
        avg = round(sum(scores) / len(scores), 2)
        result.append({
            "region": region,
            "risk": avg,
            "reports": len(scores)
        })

    return result