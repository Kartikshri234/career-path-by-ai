"""
api.py  —  FastAPI backend for CareerCompass
─────────────────────────────────────────────
Install:  pip install fastapi uvicorn
Run:      uvicorn api:app --reload
Docs:     http://localhost:8000/docs
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from career_matcher import recommend

app = FastAPI(title="CareerCompass API", version="1.0")

# Allow requests from the frontend (any origin during dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── REQUEST / RESPONSE MODELS ─────────────────────────────────────────────────

class StudentProfile(BaseModel):
    name:     str  = "Student"
    branch:   str  = ""
    cgpa:     float = 7.0
    year:     str  = ""
    leetcode: int  = 0
    github:   int  = 0
    skills:   List[str] = []


class CareerMatch(BaseModel):
    career:          str
    score:           int
    skills_have:     List[str]
    skills_missing:  List[str]
    avg_salary:      str
    demand_trend:    str


# ── ROUTES ────────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"message": "CareerCompass API is running 🚀"}


@app.post("/recommend", response_model=List[CareerMatch])
def get_recommendations(profile: StudentProfile):
    """
    Submit a student profile and receive ranked career recommendations.
    """
    student = profile.dict()
    return recommend(student)


@app.get("/careers")
def list_careers():
    """List all available career tracks."""
    from career_matcher import CAREER_PROFILES
    return [
        {"name": name, "required_skills": p["required_skills"], "avg_salary": p["avg_salary"]}
        for name, p in CAREER_PROFILES.items()
    ]
