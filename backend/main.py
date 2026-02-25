from __future__ import annotations
"""Career Readiness Scoring System - FastAPI Backend"""
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from scoring.skills_engine import get_all_skills_categorized, calculate_skills_score
from scoring.certs_engine import get_all_certifications, calculate_certs_score, scan_certificate_file
from scoring.projects_engine import calculate_projects_score
from scoring.internships_engine import calculate_internships_score
from scoring.resume_engine import calculate_resume_score
from scoring.aggregator import calculate_final_score
from scoring.suggestions import generate_suggestions

app = FastAPI(title="Career Readiness Scoring System", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"])

# --- Pydantic Models ---
class SkillsRequest(BaseModel):
    skills: List[str]

class CertRequest(BaseModel):
    name: str
    issuer: str = ""
    year: int = 2024

class CertsRequest(BaseModel):
    certifications: List[CertRequest]

class ProjectRequest(BaseModel):
    title: str
    description: str = ""
    tech_stack: List[str] = []
    github_url: str = ""

class ProjectsRequest(BaseModel):
    projects: List[ProjectRequest]

class InternshipRequest(BaseModel):
    company: str
    role: str = ""
    duration_months: int = 1
    achievements: str = ""
    has_certificate: bool = False

class InternshipsRequest(BaseModel):
    internships: List[InternshipRequest]

class ResumeTextRequest(BaseModel):
    resume_text: str

class FullScoreRequest(BaseModel):
    skills: List[str] = []
    certifications: List[CertRequest] = []
    projects: List[ProjectRequest] = []
    internships: List[InternshipRequest] = []
    resume_text: str = ""

# --- Routes ---
@app.get("/")
def root():
    return {"message": "Career Readiness Scoring System API", "version": "1.0.0"}

@app.get("/api/skills")
def get_skills():
    return get_all_skills_categorized()

@app.get("/api/certifications")
def get_certs():
    return get_all_certifications()

@app.post("/api/score/skills")
def score_skills(req: SkillsRequest):
    return calculate_skills_score(req.skills)

@app.post("/api/score/certifications")
def score_certs(req: CertsRequest):
    certs = [c.model_dump() for c in req.certifications]
    return calculate_certs_score(certs)

@app.post("/api/score/certifications/scan")
async def scan_cert_file(file: UploadFile = File(...)):
    """Upload a certificate file (PDF) to auto-detect and score the certification."""
    content = await file.read()
    return scan_certificate_file(content, filename=file.filename or "")

@app.post("/api/score/projects")
def score_projects(req: ProjectsRequest):
    projs = [p.model_dump() for p in req.projects]
    return calculate_projects_score(projs)

@app.post("/api/score/internships")
def score_internships(req: InternshipsRequest):
    interns = [i.model_dump() for i in req.internships]
    return calculate_internships_score(interns)

@app.post("/api/score/resume")
async def score_resume_file(file: UploadFile = File(...)):
    content = await file.read()
    return calculate_resume_score(file_bytes=content)

@app.post("/api/score/resume-text")
def score_resume_text(req: ResumeTextRequest):
    return calculate_resume_score(resume_text=req.resume_text)

@app.post("/api/score/calculate")
def full_calculate(req: FullScoreRequest):
    skills_result = calculate_skills_score(req.skills)
    certs_result = calculate_certs_score([c.model_dump() for c in req.certifications])
    projects_result = calculate_projects_score([p.model_dump() for p in req.projects])
    internships_result = calculate_internships_score([i.model_dump() for i in req.internships])
    resume_result = calculate_resume_score(resume_text=req.resume_text) if req.resume_text else {"score": 0, "section_scores": {}, "suggestions": ["Upload resume for scoring."]}

    component_scores = {
        "skills": skills_result["score"],
        "certifications": certs_result["score"],
        "projects": projects_result["score"],
        "internships": internships_result["score"],
        "resume": resume_result["score"],
    }
    final = calculate_final_score(component_scores)
    suggestions = generate_suggestions(component_scores)

    return {
        "final": final,
        "components": {
            "skills": skills_result,
            "certifications": certs_result,
            "projects": projects_result,
            "internships": internships_result,
            "resume": resume_result,
        },
        "suggestions": suggestions,
    }
