from __future__ import annotations
"""
Skills Scoring Engine
Evaluates technical skills based on market demand, category diversity, and depth.
Uses a pre-trained knowledge base of 500+ skills with market demand scores.
"""

import json
import os
import math

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


def load_skills_database():
    with open(os.path.join(DATA_DIR, "skills_database.json"), "r", encoding="utf-8") as f:
        return json.load(f)


def get_all_skills_categorized():
    """Return all skills organized by category for frontend dropdowns."""
    db = load_skills_database()
    result = {}
    for category, info in db["categories"].items():
        result[category] = {
            "icon": info["icon"],
            "skills": [s["name"] for s in info["skills"]]
        }
    return result


def _find_skill_info(skill_name: str, db: dict):
    """Find a skill's category and demand score using fuzzy matching."""
    skill_lower = skill_name.lower().strip()
    for category, info in db["categories"].items():
        for skill in info["skills"]:
            if skill["name"].lower() == skill_lower:
                return {
                    "name": skill["name"],
                    "category": category,
                    "demand": skill["demand"],
                    "icon": info["icon"]
                }
    # If not found in database, assign a default moderate score
    return {
        "name": skill_name,
        "category": "Other",
        "demand": 5.0,
        "icon": "🔧"
    }


def calculate_skills_score(selected_skills: list[str]) -> dict:
    """
    Calculate skills score based on:
    1. Average market demand of selected skills (40%)
    2. Category diversity - covering multiple domains (30%)
    3. Skill depth - number of skills selected (20%)
    4. High-demand skill bonus - having top-tier skills (10%)
    """
    if not selected_skills:
        return {
            "score": 0,
            "breakdown": {
                "market_demand": 0,
                "category_diversity": 0,
                "skill_depth": 0,
                "high_demand_bonus": 0
            },
            "details": [],
            "categories_covered": [],
            "suggestions": ["Start by adding your technical skills to get scored."]
        }

    db = load_skills_database()
    total_categories = len(db["categories"])

    # Analyze each skill
    skill_details = []
    categories_found = set()
    demands = []
    high_demand_count = 0

    for skill_name in selected_skills:
        info = _find_skill_info(skill_name, db)
        skill_details.append(info)
        categories_found.add(info["category"])
        demands.append(info["demand"])
        if info["demand"] >= 8.5:
            high_demand_count += 1

    # 1. Market Demand Score (average demand normalized to 0-100)
    avg_demand = sum(demands) / len(demands)
    market_demand_score = min(100, (avg_demand / 10.0) * 100)

    # 2. Category Diversity Score
    diversity_ratio = len(categories_found) / min(total_categories, 6)  # Expect up to 6 categories
    diversity_score = min(100, diversity_ratio * 100)

    # 3. Skill Depth Score (logarithmic scale, optimal around 15-25 skills)
    optimal_skills = 20
    depth_raw = min(len(selected_skills) / optimal_skills, 1.5)
    depth_score = min(100, depth_raw * 75 + (25 if len(selected_skills) >= 5 else 0))

    # 4. High Demand Bonus
    high_demand_ratio = high_demand_count / max(len(selected_skills), 1)
    high_demand_score = min(100, high_demand_ratio * 120)  # Slight bonus for high concentration

    # Weighted final score
    final_score = (
        market_demand_score * 0.40 +
        diversity_score * 0.30 +
        depth_score * 0.20 +
        high_demand_score * 0.10
    )
    final_score = min(100, round(final_score, 1))

    # Generate suggestions
    suggestions = []
    if len(selected_skills) < 5:
        suggestions.append("Add more skills — aim for at least 10-15 technical skills.")
    if len(categories_found) < 3:
        suggestions.append("Diversify your skillset across more technology categories.")
    if high_demand_count < 3:
        suggestions.append("Focus on learning high-demand skills like Python, React.js, AWS, or Docker.")
    if avg_demand < 7:
        suggestions.append("Consider upgrading to more in-demand technologies.")
    if "Artificial Intelligence & ML" not in categories_found:
        suggestions.append("AI/ML skills are extremely in-demand — consider adding some.")
    if "Cloud Computing" not in categories_found and "DevOps & CI/CD" not in categories_found:
        suggestions.append("Cloud and DevOps skills significantly boost career readiness.")

    return {
        "score": final_score,
        "breakdown": {
            "market_demand": round(market_demand_score, 1),
            "category_diversity": round(diversity_score, 1),
            "skill_depth": round(depth_score, 1),
            "high_demand_bonus": round(high_demand_score, 1)
        },
        "details": skill_details,
        "categories_covered": list(categories_found),
        "total_skills": len(selected_skills),
        "suggestions": suggestions
    }
