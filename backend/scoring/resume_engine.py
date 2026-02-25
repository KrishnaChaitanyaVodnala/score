"""Resume ATS Scoring Engine - Parses PDFs and scores against ATS criteria."""
import re, io

try:
    from pdfminer.high_level import extract_text
    from pdfminer.layout import LAParams
    PDF_OK = True
except ImportError:
    PDF_OK = False

SECTION_HEADERS = {
    "contact": ["contact", "personal"],
    "summary": ["summary", "professional summary", "objective", "career objective", "about me", "profile"],
    "experience": ["experience", "work experience", "professional experience", "employment", "internship"],
    "education": ["education", "academic", "qualifications", "degrees"],
    "skills": ["skills", "technical skills", "competencies", "technologies", "tools", "tech stack"],
    "certifications": ["certifications", "certificates", "credentials", "professional development"],
    "projects": ["projects", "personal projects", "academic projects", "portfolio"],
}

QUALITY_KW = {
    "experience": ["developed", "implemented", "designed", "managed", "led", "built", "created", "improved", "increased", "reduced", "optimized", "architected", "deployed", "automated", "collaborated", "mentored"],
    "education": ["bachelor", "master", "phd", "b.tech", "m.tech", "b.e", "m.e", "gpa", "cgpa", "university", "institute", "college"],
    "skills": ["python", "java", "javascript", "react", "node", "sql", "aws", "docker", "kubernetes", "git", "linux", "machine learning", "data", "cloud", "agile", "api"],
    "summary": ["experienced", "passionate", "skilled", "proficient", "expertise", "results-driven", "innovative"],
    "certifications": ["certified", "aws", "azure", "google cloud", "comptia", "pmp", "scrum"],
    "projects": ["built", "developed", "created", "github", "deployed", "full-stack", "machine learning", "web", "mobile"],
}

def _extract_pdf(fb):
    if not PDF_OK: return ""
    try: return extract_text(io.BytesIO(fb), laparams=LAParams())
    except: return ""

def _score_contact(text):
    s, found, missing = 0, {}, []
    checks = [("email", r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', 25),
              ("phone", r'[\+]?[(]?[0-9]{1,4}[)]?[-\s\./0-9]{7,15}', 25),
              ("linkedin", r'linkedin\.com/in/[\w\-]+', 20),
              ("github", r'github\.com/[\w\-]+', 20),
              ("portfolio", r'https?://[\w\-\.]+\.\w{2,}', 10)]
    for name, pat, pts in checks:
        if re.search(pat, text, re.I):
            found[name] = True; s += pts
        else: missing.append(name)
    return {"score": min(100, s), "found": found, "missing": missing,
            "feedback": f"Found {len(found)}/5 contact elements." + (f" Missing: {', '.join(missing)}" if missing else " Complete!")}

def _score_section(text, key):
    tl = text.lower(); lines = tl.split('\n')
    headers = SECTION_HEADERS.get(key, [])
    kws = QUALITY_KW.get(key, [])
    sec_found = any(h in l.strip() for h in headers for l in lines)
    if not sec_found:
        ct = sum(1 for k in kws if k in tl)
        if ct > 2: sec_found = True
    if not sec_found:
        return {"score": 0, "section_found": False, "quality_indicators": 0,
                "feedback": f"Add a '{headers[0].title() if headers else key}' section to your resume."}
    found_kw = [k for k in kws if k in tl]
    ratio = len(found_kw) / max(len(kws), 1)
    score = min(100, ratio * 80 + 20)
    return {"score": round(score, 1), "section_found": True, "quality_indicators": len(found_kw),
            "quality_details": found_kw[:8],
            "feedback": f"Found {len(found_kw)} quality indicators." + (" Strong!" if score >= 70 else " Add more detail.")}

def _score_formatting(text):
    words = text.split(); wc = len(words)
    lines = [l for l in text.split('\n') if l.strip()]
    s, fb = 0, []
    if 300 <= wc <= 1200: s += 30; fb.append("✅ Good length")
    elif wc < 300: s += 10; fb.append("⚠️ Too short")
    else: s += 20; fb.append("⚠️ May be too long")
    sec_ct = sum(1 for hs in SECTION_HEADERS.values() if any(h in text.lower() for h in hs))
    if sec_ct >= 5: s += 30; fb.append("✅ Good sections")
    elif sec_ct >= 3: s += 20; fb.append("⚠️ Add more sections")
    else: s += 10; fb.append("❌ Missing sections")
    bullets = sum(1 for l in lines if l.strip()[:1] in '•-●■→*')
    if bullets >= 5: s += 20; fb.append("✅ Good bullet points")
    elif bullets >= 2: s += 10; fb.append("⚠️ More bullets needed")
    else: s += 5; fb.append("❌ Add bullet points")
    nums = len(re.findall(r'\d+[%+]?', text))
    if nums >= 5: s += 20; fb.append("✅ Good metrics")
    elif nums >= 2: s += 10; fb.append("⚠️ Add metrics")
    else: fb.append("❌ Add quantifiable results")
    return {"score": min(100, s), "total_words": wc, "sections_detected": sec_ct,
            "bullet_points": bullets, "metrics_found": nums, "feedback": fb}

def calculate_resume_score(file_bytes=None, resume_text=None):
    if file_bytes:
        text = _extract_pdf(file_bytes)
        if not text: return {"score": 0, "error": "Could not extract text from PDF.",
            "section_scores": {}, "suggestions": ["Upload a text-based PDF."]}
    elif resume_text: text = resume_text
    else: return {"score": 0, "section_scores": {}, "suggestions": ["Upload your resume."]}

    cr = _score_contact(text)
    fm = _score_formatting(text)
    sections = {
        "Contact Information": {"score": cr["score"], "weight": 10, "details": cr},
        "Professional Summary": {"score": _score_section(text, "summary")["score"], "weight": 15, "details": _score_section(text, "summary")},
        "Work Experience": {"score": _score_section(text, "experience")["score"], "weight": 25, "details": _score_section(text, "experience")},
        "Education": {"score": _score_section(text, "education")["score"], "weight": 15, "details": _score_section(text, "education")},
        "Skills": {"score": _score_section(text, "skills")["score"], "weight": 15, "details": _score_section(text, "skills")},
        "Certifications": {"score": _score_section(text, "certifications")["score"], "weight": 5, "details": _score_section(text, "certifications")},
        "Projects": {"score": _score_section(text, "projects")["score"], "weight": 10, "details": _score_section(text, "projects")},
        "Formatting & Structure": {"score": fm["score"], "weight": 5, "details": fm},
    }
    tw = sum(s["score"] * s["weight"] for s in sections.values())
    total_w = sum(s["weight"] for s in sections.values())
    overall = round(tw / max(total_w, 1), 1)

    sugg = []
    for name, sd in sorted(sections.items(), key=lambda x: x[1]["score"]):
        if sd["score"] < 60:
            sugg.append(f"Improve '{name}' section (scored {sd['score']}/100).")
    if overall >= 80: sugg.insert(0, "Excellent resume! Fine-tune weak sections.")
    elif overall >= 60: sugg.insert(0, "Good foundation. Focus on weak areas.")
    else: sugg.insert(0, "Resume needs improvement. Address each section.")
    return {"score": overall, "section_scores": sections, "total_words": fm["total_words"], "suggestions": sugg}
