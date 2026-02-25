"""Weighted Score Aggregator - Combines all 5 component scores into final career readiness score."""

WEIGHTS = {
    "skills": 30,
    "certifications": 15,
    "projects": 25,
    "internships": 20,
    "resume": 10,
}

def get_grade(score):
    if score >= 90: return {"grade": "A+", "label": "Exceptional", "color": "#10b981"}
    if score >= 80: return {"grade": "A", "label": "Excellent", "color": "#22c55e"}
    if score >= 70: return {"grade": "B+", "label": "Very Good", "color": "#84cc16"}
    if score >= 60: return {"grade": "B", "label": "Good", "color": "#eab308"}
    if score >= 50: return {"grade": "C+", "label": "Average", "color": "#f97316"}
    if score >= 40: return {"grade": "C", "label": "Below Average", "color": "#ef4444"}
    if score >= 30: return {"grade": "D", "label": "Needs Work", "color": "#dc2626"}
    return {"grade": "F", "label": "Critical", "color": "#991b1b"}

def calculate_final_score(component_scores: dict) -> dict:
    """
    Calculate the weighted final career readiness score.
    component_scores: {"skills": 75.5, "certifications": 60.0, ...}
    """
    weighted_sum = 0
    total_weight = 0
    component_breakdown = {}

    for component, weight in WEIGHTS.items():
        raw_score = component_scores.get(component, 0)
        weighted_contribution = (raw_score * weight) / 100
        weighted_sum += weighted_contribution
        total_weight += weight
        component_breakdown[component] = {
            "raw_score": round(raw_score, 1),
            "weight": weight,
            "weighted_score": round(weighted_contribution, 1),
            "grade": get_grade(raw_score),
        }

    final_score = round(weighted_sum, 1)
    overall_grade = get_grade(final_score)

    # Find strongest and weakest areas
    sorted_components = sorted(component_breakdown.items(), key=lambda x: x[1]["raw_score"])
    weakest = sorted_components[:2]
    strongest = sorted_components[-2:]

    return {
        "final_score": final_score,
        "max_score": 100,
        "overall_grade": overall_grade,
        "weights": WEIGHTS,
        "component_breakdown": component_breakdown,
        "strongest_areas": [{"name": n, "score": d["raw_score"]} for n, d in reversed(strongest)],
        "weakest_areas": [{"name": n, "score": d["raw_score"]} for n, d in weakest],
    }
