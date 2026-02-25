from __future__ import annotations
"""
Internships Scoring Engine
Evaluates internships based on company recognition, role relevance,
duration, achievements, and overall quality.
"""

from difflib import SequenceMatcher

# Company tier database
COMPANY_TIERS = {
    "tier_1": {
        "value": 10,
        "label": "FAANG / Top Tech Giants",
        "companies": [
            "google", "meta", "facebook", "amazon", "apple", "microsoft",
            "netflix", "nvidia", "tesla", "openai", "deepmind", "anthropic",
            "salesforce", "adobe", "oracle", "ibm", "intel", "qualcomm",
            "samsung", "sony", "uber", "airbnb", "twitter", "x corp",
            "linkedin", "spotify", "stripe", "palantir", "snowflake",
            "databricks", "coinbase", "bytedance", "tiktok"
        ]
    },
    "tier_2": {
        "value": 8,
        "label": "Top Companies / Unicorns",
        "companies": [
            "accenture", "deloitte", "mckinsey", "bcg", "pwc", "ernst & young",
            "kpmg", "capgemini", "infosys", "tcs", "wipro", "hcl",
            "cognizant", "tech mahindra", "mindtree", "mphasis",
            "vmware", "servicenow", "workday", "atlassian", "twilio",
            "cloudflare", "hashicorp", "elastic", "mongodb inc",
            "shopify", "pinterest", "snap", "discord", "github",
            "gitlab", "vercel", "figma", "notion", "canva",
            "razorpay", "paytm", "phonepe", "cred", "swiggy",
            "zomato", "flipkart", "ola", "byjus", "unacademy",
            "meesho", "dream11", "groww", "zerodha", "freshworks",
            "zoho", "postman", "browserstack", "druva",
            "samsung", "lg", "bosch", "siemens", "ge",
            "jpmorgan", "goldman sachs", "morgan stanley", "citi",
            "barclays", "deutsche bank", "credit suisse", "hsbc",
            "visa", "mastercard", "paypal", "square", "robinhood"
        ]
    },
    "tier_3": {
        "value": 6,
        "label": "Established Companies / Mid-tier",
        "companies": [
            "startups", "mid-size companies", "regional companies",
            "consulting firms", "digital agencies", "it services"
        ]
    },
    "tier_4": {
        "value": 4,
        "label": "Startups / Small Companies",
        "companies": []
    }
}

# Role relevance keywords with weights
ROLE_KEYWORDS = {
    "software engineer": 10, "software developer": 10,
    "full stack": 9, "frontend": 8, "backend": 8,
    "data scientist": 10, "data analyst": 8, "data engineer": 9,
    "ml engineer": 10, "machine learning": 10, "ai engineer": 10,
    "devops": 9, "cloud engineer": 9, "sre": 9,
    "security": 8, "cybersecurity": 9, "penetration tester": 8,
    "product manager": 8, "project manager": 7,
    "mobile developer": 8, "ios developer": 8, "android developer": 8,
    "blockchain developer": 7, "web3": 7,
    "research": 8, "researcher": 8, "intern": 5,
    "technical": 7, "engineering": 7, "developer": 7,
    "analyst": 6, "associate": 5, "trainee": 4,
    "qa engineer": 7, "test engineer": 7, "automation": 7,
    "ui/ux": 7, "designer": 6,
    "system administrator": 6, "network engineer": 7,
    "database administrator": 7, "dba": 7,
}

# Achievement keywords
ACHIEVEMENT_KEYWORDS = {
    "led": 3, "managed": 3, "architected": 4, "designed": 3,
    "built": 2, "developed": 2, "implemented": 2, "created": 2,
    "improved": 3, "increased": 3, "reduced": 3, "optimized": 3,
    "automated": 3, "streamlined": 2, "launched": 3, "deployed": 2,
    "mentored": 3, "collaborated": 2, "presented": 2, "published": 3,
    "awarded": 4, "recognized": 3, "promoted": 3, "selected": 2,
    "patent": 4, "paper": 3, "conference": 3, "hackathon": 2,
    "revenue": 3, "users": 2, "performance": 2, "scalability": 3,
    "million": 3, "thousand": 2, "percent": 2, "%": 2,
    "first place": 4, "winner": 3, "top": 2, "best": 2,
    "open source": 3, "contribution": 2, "community": 2,
}


def _identify_company_tier(company_name: str) -> dict:
    """Identify the tier of a company using fuzzy matching."""
    company_lower = company_name.lower().strip()

    for tier_key, tier_info in COMPANY_TIERS.items():
        for known in tier_info["companies"]:
            if known in company_lower or company_lower in known:
                return {
                    "tier": tier_key,
                    "tier_label": tier_info["label"],
                    "tier_value": tier_info["value"]
                }
            ratio = SequenceMatcher(None, company_lower, known).ratio()
            if ratio >= 0.8:
                return {
                    "tier": tier_key,
                    "tier_label": tier_info["label"],
                    "tier_value": tier_info["value"]
                }

    # Default to tier_3 for unknown companies (assume mid-tier)
    return {
        "tier": "tier_3",
        "tier_label": COMPANY_TIERS["tier_3"]["label"],
        "tier_value": COMPANY_TIERS["tier_3"]["value"]
    }


def _score_role(role: str) -> float:
    """Score the relevance and seniority of the internship role."""
    if not role:
        return 30

    role_lower = role.lower()
    max_score = 0
    for keyword, weight in ROLE_KEYWORDS.items():
        if keyword in role_lower:
            max_score = max(max_score, weight)

    return min(100, max_score * 10)


def _score_achievements(achievements: str) -> dict:
    """Score the quality of described achievements."""
    if not achievements:
        return {"score": 15, "keywords_found": [], "word_count": 0}

    ach_lower = achievements.lower()
    words = ach_lower.split()
    word_count = len(words)

    keywords_found = []
    total_weight = 0
    for keyword, weight in ACHIEVEMENT_KEYWORDS.items():
        if keyword in ach_lower:
            keywords_found.append(keyword)
            total_weight += weight

    # Score based on keywords and description length
    keyword_score = min(100, (total_weight / 20.0) * 100)
    length_bonus = min(30, (word_count / 50.0) * 30)

    score = min(100, keyword_score * 0.7 + length_bonus + 10)

    return {
        "score": round(score, 1),
        "keywords_found": keywords_found,
        "word_count": word_count
    }


def _score_duration(duration_months: int) -> float:
    """Score based on internship duration."""
    if duration_months >= 12:
        return 100
    elif duration_months >= 6:
        return 90
    elif duration_months >= 3:
        return 70
    elif duration_months >= 2:
        return 55
    elif duration_months >= 1:
        return 40
    return 20


def calculate_internships_score(internships: list[dict]) -> dict:
    """
    Calculate internship score based on:
    1. Company recognition/tier (30%)
    2. Role relevance (25%)
    3. Duration (15%)
    4. Achievements quality (20%)
    5. Quantity of internships (10%)

    Each internship: {
        "company": "Google", "role": "Software Engineer Intern",
        "duration_months": 3, "achievements": "Built microservices...",
        "has_certificate": true
    }
    """
    if not internships:
        return {
            "score": 0,
            "breakdown": {
                "company_recognition": 0,
                "role_relevance": 0,
                "duration": 0,
                "achievements": 0,
                "quantity": 0
            },
            "internship_details": [],
            "suggestions": ["Pursue internships to gain real-world experience and boost your career readiness."]
        }

    internship_details = []
    company_scores = []
    role_scores = []
    duration_scores = []
    achievement_scores = []

    for intern in internships:
        company = intern.get("company", "Unknown")
        role = intern.get("role", "")
        duration_months = intern.get("duration_months", 1)
        achievements = intern.get("achievements", "")
        has_certificate = intern.get("has_certificate", False)

        company_tier = _identify_company_tier(company)
        role_score = _score_role(role)
        dur_score = _score_duration(duration_months)
        ach_result = _score_achievements(achievements)

        company_score = company_tier["tier_value"] * 10
        cert_bonus = 5 if has_certificate else 0

        individual_score = (
            company_score * 0.30 +
            role_score * 0.25 +
            dur_score * 0.15 +
            ach_result["score"] * 0.20 +
            cert_bonus
        )

        internship_details.append({
            "company": company,
            "role": role,
            "duration_months": duration_months,
            "company_tier": company_tier,
            "role_score": round(role_score, 1),
            "duration_score": round(dur_score, 1),
            "achievement_analysis": ach_result,
            "has_certificate": has_certificate,
            "individual_score": round(individual_score, 1)
        })

        company_scores.append(company_score)
        role_scores.append(role_score)
        duration_scores.append(dur_score)
        achievement_scores.append(ach_result["score"])

    num_internships = len(internships)

    # Aggregate
    avg_company = sum(company_scores) / len(company_scores)
    avg_role = sum(role_scores) / len(role_scores)
    avg_duration = sum(duration_scores) / len(duration_scores)
    avg_achievement = sum(achievement_scores) / len(achievement_scores)

    # Quantity score
    if num_internships >= 4:
        quantity_score = 100
    elif num_internships >= 3:
        quantity_score = 85
    elif num_internships >= 2:
        quantity_score = 70
    else:
        quantity_score = 45

    # Weighted final
    final_score = (
        avg_company * 0.30 +
        avg_role * 0.25 +
        avg_duration * 0.15 +
        avg_achievement * 0.20 +
        quantity_score * 0.10
    )
    final_score = min(100, round(final_score, 1))

    # Suggestions
    suggestions = []
    if num_internships < 2:
        suggestions.append("Aim for at least 2-3 internships before graduation.")
    if avg_company < 60:
        suggestions.append("Target internships at top-tier or well-known companies for higher impact.")
    if avg_achievement < 50:
        suggestions.append("Document your internship achievements with quantifiable metrics (e.g., 'improved performance by 30%').")
    if avg_duration < 60:
        suggestions.append("Longer internships (3-6 months) carry more weight than short ones.")
    if any(not i.get("has_certificate", False) for i in internships):
        suggestions.append("Obtain completion certificates for all internships.")

    return {
        "score": final_score,
        "breakdown": {
            "company_recognition": round(avg_company, 1),
            "role_relevance": round(avg_role, 1),
            "duration": round(avg_duration, 1),
            "achievements": round(avg_achievement, 1),
            "quantity": round(quantity_score, 1)
        },
        "internship_details": internship_details,
        "total_internships": num_internships,
        "suggestions": suggestions
    }
