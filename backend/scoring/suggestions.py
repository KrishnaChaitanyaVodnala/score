"""Improvement Suggestions Generator - Analyzes weak areas and provides actionable recommendations."""

SUGGESTION_DB = {
    "skills": {
        "high": [
            {"text": "Excellent skill portfolio! Consider specializing deeper in one domain.", "impact": "low"},
            {"text": "Explore emerging technologies like Generative AI, Edge Computing, or Quantum Computing.", "impact": "medium"},
        ],
        "medium": [
            {"text": "Learn at least one cloud platform (AWS/Azure/GCP) — cloud skills are essential.", "impact": "high"},
            {"text": "Add DevOps tools (Docker, Kubernetes, CI/CD) to your skillset.", "impact": "high"},
            {"text": "Diversify across categories: frontend + backend + cloud = full-stack readiness.", "impact": "high"},
            {"text": "Focus on Python and JavaScript — the two most in-demand languages.", "impact": "medium"},
        ],
        "low": [
            {"text": "Start with foundational programming languages: Python, JavaScript, or Java.", "impact": "high"},
            {"text": "Learn web development basics: HTML, CSS, React or Angular.", "impact": "high"},
            {"text": "Take structured courses on platforms like Coursera, Udemy, or freeCodeCamp.", "impact": "high"},
            {"text": "Build a learning roadmap — aim for 10+ skills across 3+ categories.", "impact": "high"},
            {"text": "Join coding communities (GitHub, Stack Overflow, Dev.to) to accelerate learning.", "impact": "medium"},
        ],
    },
    "certifications": {
        "high": [
            {"text": "Great certifications! Aim for a Platinum-tier cert (AWS Pro, CISSP, CKA).", "impact": "medium"},
            {"text": "Keep certifications current — renew before they expire.", "impact": "low"},
        ],
        "medium": [
            {"text": "Pursue at least one Gold-tier certification (AWS Associate, Azure, CompTIA Security+).", "impact": "high"},
            {"text": "Prioritize vendor-neutral certs that are widely recognized across industries.", "impact": "medium"},
            {"text": "Get 3-5 certifications across different domains for maximum impact.", "impact": "high"},
        ],
        "low": [
            {"text": "Start with AWS Cloud Practitioner or Azure Fundamentals — affordable and highly valued.", "impact": "high"},
            {"text": "Complete Coursera/edX specializations from top universities for credibility.", "impact": "high"},
            {"text": "Free certifications from Google, IBM, or Microsoft are great starting points.", "impact": "high"},
            {"text": "Certifications demonstrate commitment — even entry-level ones matter.", "impact": "medium"},
        ],
    },
    "projects": {
        "high": [
            {"text": "Strong project portfolio! Contribute to open-source projects for extra impact.", "impact": "medium"},
            {"text": "Write detailed READMEs and documentation for each project.", "impact": "medium"},
            {"text": "Deploy projects live (Vercel, AWS, Heroku) so recruiters can see them in action.", "impact": "medium"},
        ],
        "medium": [
            {"text": "Build 2-3 more projects using advanced concepts (microservices, ML, real-time).", "impact": "high"},
            {"text": "Put ALL projects on GitHub with clean code, READMEs, and proper commit history.", "impact": "high"},
            {"text": "Use modern tech stacks in projects: React + Node.js + Docker + AWS.", "impact": "high"},
            {"text": "Include at least one full-stack project with frontend, backend, and database.", "impact": "high"},
        ],
        "low": [
            {"text": "Start building projects NOW — they're the #1 way to demonstrate capability.", "impact": "high"},
            {"text": "Begin with 3 projects: a web app, an API, and a data/ML project.", "impact": "high"},
            {"text": "Clone and improve popular open-source projects to learn best practices.", "impact": "high"},
            {"text": "Create a GitHub profile README showcasing your best work.", "impact": "medium"},
            {"text": "Build a personal portfolio website — it IS a project too!", "impact": "high"},
        ],
    },
    "internships": {
        "high": [
            {"text": "Excellent internship experience! Document achievements quantifiably on your resume.", "impact": "medium"},
            {"text": "Seek a return offer or full-time conversion from your best internship.", "impact": "high"},
        ],
        "medium": [
            {"text": "Apply to internships at top-tier companies (FAANG, top unicorns).", "impact": "high"},
            {"text": "Aim for 3-6 month internships — they carry significantly more weight.", "impact": "high"},
            {"text": "Document internship achievements with metrics: 'Reduced load time by 40%'.", "impact": "high"},
            {"text": "Get LinkedIn recommendations from internship supervisors.", "impact": "medium"},
        ],
        "low": [
            {"text": "Apply widely to internships — even small company internships build experience.", "impact": "high"},
            {"text": "Explore virtual/remote internships — many top companies offer them.", "impact": "high"},
            {"text": "Start with contributing to open source if internships are hard to find.", "impact": "medium"},
            {"text": "Participate in programs like Google Summer of Code, MLH Fellowship, or LFX.", "impact": "high"},
            {"text": "Volunteer for tech projects at university clubs or local organizations.", "impact": "medium"},
        ],
    },
    "resume": {
        "high": [
            {"text": "Well-structured resume! Keep it updated with latest achievements.", "impact": "low"},
            {"text": "Tailor your resume for each job application using relevant keywords.", "impact": "medium"},
        ],
        "medium": [
            {"text": "Add more action verbs: 'Developed', 'Architected', 'Optimized', 'Led'.", "impact": "high"},
            {"text": "Include quantifiable results: numbers, percentages, and metrics.", "impact": "high"},
            {"text": "Ensure all sections are present: Summary, Experience, Education, Skills, Projects.", "impact": "high"},
            {"text": "Add LinkedIn and GitHub URLs to your contact section.", "impact": "medium"},
        ],
        "low": [
            {"text": "Create a professional resume using a clean, ATS-friendly template.", "impact": "high"},
            {"text": "Structure with clear sections: Contact → Summary → Experience → Education → Skills.", "impact": "high"},
            {"text": "Use bullet points with action verbs for each experience entry.", "impact": "high"},
            {"text": "Keep it to 1 page (students) or 2 pages (experienced) — no more.", "impact": "high"},
            {"text": "Use a PDF format to preserve formatting across systems.", "impact": "medium"},
        ],
    },
}

def generate_suggestions(component_scores: dict) -> dict:
    """Generate prioritized improvement suggestions based on component scores."""
    all_suggestions = []
    priority_order = []

    # Sort components by score (weakest first)
    sorted_components = sorted(component_scores.items(), key=lambda x: x[1])

    for component, score in sorted_components:
        if component not in SUGGESTION_DB:
            continue
        if score >= 75:
            level = "high"
        elif score >= 45:
            level = "medium"
        else:
            level = "low"

        suggestions = SUGGESTION_DB[component][level]
        for s in suggestions:
            all_suggestions.append({
                "component": component,
                "score": score,
                "level": level,
                "text": s["text"],
                "impact": s["impact"],
            })
        priority_order.append({"component": component, "score": score, "level": level})

    # Sort by impact (high first) then by component score (low first)
    impact_order = {"high": 0, "medium": 1, "low": 2}
    all_suggestions.sort(key=lambda x: (impact_order.get(x["impact"], 2), x["score"]))

    # Top priority actions
    top_actions = [s for s in all_suggestions if s["impact"] == "high"][:5]

    return {
        "all_suggestions": all_suggestions,
        "top_priority_actions": top_actions,
        "priority_order": priority_order,
        "total_suggestions": len(all_suggestions),
    }
