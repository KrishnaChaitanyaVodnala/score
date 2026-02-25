from __future__ import annotations
"""
Projects Scoring Engine
Evaluates projects based on description quality, technical depth, GitHub presence,
and quantity. Uses NLP keyword analysis and TF-IDF scoring.
"""

import re
import math

# Technical keywords and their weights for project analysis
TECH_KEYWORDS = {
    # Architecture patterns
    "microservices": 3, "serverless": 3, "event-driven": 3, "distributed": 3,
    "real-time": 2, "scalable": 2, "high-availability": 3, "fault-tolerant": 3,
    "load balancing": 2, "caching": 2, "message queue": 2, "api gateway": 2,

    # AI/ML
    "machine learning": 3, "deep learning": 3, "neural network": 3,
    "natural language processing": 3, "nlp": 2, "computer vision": 3,
    "tensorflow": 2, "pytorch": 2, "transformer": 3, "bert": 2, "gpt": 2,
    "recommendation system": 3, "classification": 2, "regression": 2,
    "clustering": 2, "reinforcement learning": 3, "generative ai": 3,
    "llm": 3, "fine-tuning": 2, "rag": 2,

    # Web/Mobile
    "react": 2, "angular": 2, "vue": 2, "next.js": 2, "node.js": 2,
    "express": 1, "django": 2, "flask": 1, "fastapi": 2, "spring boot": 2,
    "graphql": 2, "rest api": 2, "websocket": 2, "progressive web app": 2,
    "responsive": 1, "authentication": 2, "oauth": 2, "jwt": 2,

    # Mobile
    "react native": 2, "flutter": 2, "ios": 2, "android": 2, "mobile": 1,
    "cross-platform": 2,

    # Data
    "big data": 2, "data pipeline": 2, "etl": 2, "data warehouse": 2,
    "analytics": 2, "visualization": 1, "dashboard": 1, "reporting": 1,
    "spark": 2, "hadoop": 2, "kafka": 2, "elasticsearch": 2,

    # Cloud/DevOps
    "aws": 2, "azure": 2, "gcp": 2, "docker": 2, "kubernetes": 3,
    "ci/cd": 2, "terraform": 2, "infrastructure as code": 2,
    "cloud-native": 2, "monitoring": 1, "logging": 1,

    # Security
    "security": 2, "encryption": 2, "authentication": 2, "penetration testing": 3,
    "vulnerability": 2, "firewall": 2, "zero trust": 2,

    # Blockchain
    "blockchain": 2, "smart contract": 2, "solidity": 2, "defi": 2,
    "web3": 2, "nft": 1, "decentralized": 2,

    # Quality indicators
    "testing": 1, "unit test": 2, "integration test": 2, "tdd": 2,
    "ci/cd pipeline": 2, "automated": 1, "performance": 1, "optimization": 2,
    "documentation": 1, "open source": 2, "contributor": 1,

    # Database
    "postgresql": 1, "mongodb": 1, "redis": 1, "mysql": 1,
    "database design": 2, "sql": 1, "nosql": 1, "orm": 1,

    # Advanced concepts
    "algorithm": 2, "data structure": 2, "design pattern": 2,
    "system design": 3, "architecture": 2, "concurrency": 2,
    "multithreading": 2, "async": 1, "parallel": 2,
}

GITHUB_URL_PATTERN = re.compile(r'https?://github\.com/[\w\-]+/[\w\-]+', re.IGNORECASE)


def _analyze_description(description: str) -> dict:
    """Analyze project description for technical depth and quality."""
    if not description:
        return {"keyword_score": 0, "length_score": 0, "keywords_found": []}

    desc_lower = description.lower()
    words = desc_lower.split()
    word_count = len(words)

    # Keyword analysis
    keywords_found = []
    total_keyword_weight = 0
    for keyword, weight in TECH_KEYWORDS.items():
        if keyword in desc_lower:
            keywords_found.append({"keyword": keyword, "weight": weight})
            total_keyword_weight += weight

    # Normalize keyword score (max around 30 weight points for excellent projects)
    keyword_score = min(100, (total_keyword_weight / 25.0) * 100)

    # Description length score
    if word_count >= 100:
        length_score = 100
    elif word_count >= 50:
        length_score = 80
    elif word_count >= 25:
        length_score = 60
    elif word_count >= 10:
        length_score = 40
    else:
        length_score = 20

    return {
        "keyword_score": round(keyword_score, 1),
        "length_score": round(length_score, 1),
        "keywords_found": keywords_found,
        "word_count": word_count
    }


def _analyze_tech_stack(tech_stack: list[str]) -> dict:
    """Analyze the technical stack used in the project."""
    if not tech_stack:
        return {"score": 0, "diversity": 0}

    stack_count = len(tech_stack)

    # Tech stack diversity and quality
    high_demand_techs = {
        "react", "angular", "vue", "next.js", "node.js", "python", "django",
        "flask", "fastapi", "spring boot", "docker", "kubernetes", "aws",
        "azure", "gcp", "tensorflow", "pytorch", "postgresql", "mongodb",
        "redis", "graphql", "typescript", "go", "rust", "kafka"
    }

    high_demand_count = sum(
        1 for t in tech_stack if t.lower() in high_demand_techs
    )

    if stack_count >= 6:
        diversity_score = 100
    elif stack_count >= 4:
        diversity_score = 80
    elif stack_count >= 2:
        diversity_score = 60
    else:
        diversity_score = 35

    demand_ratio = high_demand_count / max(stack_count, 1)
    demand_score = min(100, demand_ratio * 110)

    score = diversity_score * 0.5 + demand_score * 0.5

    return {
        "score": round(score, 1),
        "diversity": stack_count,
        "high_demand_count": high_demand_count
    }


def calculate_projects_score(projects: list[dict]) -> dict:
    """
    Calculate projects score based on:
    1. Technical depth of descriptions (35%)
    2. Tech stack quality and diversity (20%)
    3. GitHub presence and links (20%)
    4. Project quantity and variety (25%)

    Each project: {"title": "...", "description": "...", "tech_stack": [...], "github_url": "..."}
    """
    if not projects:
        return {
            "score": 0,
            "breakdown": {
                "technical_depth": 0,
                "tech_stack_quality": 0,
                "github_presence": 0,
                "project_quantity": 0
            },
            "project_details": [],
            "suggestions": ["Start building projects to demonstrate your skills!"]
        }

    project_details = []
    depth_scores = []
    stack_scores = []
    github_count = 0

    for proj in projects:
        title = proj.get("title", "Untitled")
        description = proj.get("description", "")
        tech_stack = proj.get("tech_stack", [])
        github_url = proj.get("github_url", "")

        desc_analysis = _analyze_description(description)
        stack_analysis = _analyze_tech_stack(tech_stack)
        has_github = bool(github_url and GITHUB_URL_PATTERN.match(github_url))

        if has_github:
            github_count += 1

        # Individual project score
        proj_score = (
            desc_analysis["keyword_score"] * 0.4 +
            desc_analysis["length_score"] * 0.2 +
            stack_analysis["score"] * 0.3 +
            (100 if has_github else 20) * 0.1
        )

        project_details.append({
            "title": title,
            "score": round(proj_score, 1),
            "description_analysis": desc_analysis,
            "tech_stack_analysis": stack_analysis,
            "has_github": has_github,
            "github_url": github_url
        })

        depth_scores.append(desc_analysis["keyword_score"])
        stack_scores.append(stack_analysis["score"])

    # Aggregate scores
    num_projects = len(projects)

    # 1. Technical Depth (average of all project keyword scores)
    avg_depth = sum(depth_scores) / len(depth_scores) if depth_scores else 0
    technical_depth = min(100, avg_depth)

    # 2. Tech Stack Quality
    avg_stack = sum(stack_scores) / len(stack_scores) if stack_scores else 0
    tech_stack_quality = min(100, avg_stack)

    # 3. GitHub Presence
    github_ratio = github_count / max(num_projects, 1)
    github_presence = min(100, github_ratio * 110)

    # 4. Project Quantity
    if num_projects >= 8:
        project_quantity = 100
    elif num_projects >= 5:
        project_quantity = 85
    elif num_projects >= 3:
        project_quantity = 70
    elif num_projects >= 2:
        project_quantity = 55
    else:
        project_quantity = 35

    # Weighted final
    final_score = (
        technical_depth * 0.35 +
        tech_stack_quality * 0.20 +
        github_presence * 0.20 +
        project_quantity * 0.25
    )
    final_score = min(100, round(final_score, 1))

    # Suggestions
    suggestions = []
    if num_projects < 3:
        suggestions.append("Build at least 3-5 diverse projects to showcase your abilities.")
    if github_count < num_projects:
        suggestions.append("Host all your projects on GitHub with proper README documentation.")
    if avg_depth < 50:
        suggestions.append("Work on more technically complex projects using advanced concepts (microservices, ML, etc.).")
    if avg_stack < 50:
        suggestions.append("Use high-demand technologies in your projects (React, Node.js, Docker, AWS, etc.).")
    if num_projects >= 3 and avg_depth >= 60:
        suggestions.append("Great project portfolio! Consider contributing to open-source projects for extra impact.")

    return {
        "score": final_score,
        "breakdown": {
            "technical_depth": round(technical_depth, 1),
            "tech_stack_quality": round(tech_stack_quality, 1),
            "github_presence": round(github_presence, 1),
            "project_quantity": round(project_quantity, 1)
        },
        "project_details": project_details,
        "total_projects": num_projects,
        "suggestions": suggestions
    }
