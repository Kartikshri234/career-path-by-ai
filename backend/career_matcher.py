"""
career_matcher.py
─────────────────
Core ML-style scoring engine for the Career Path Recommendation System.
No external ML libraries needed — pure Python weighted scoring.
Run:  python career_matcher.py
"""

# ── DATA ──────────────────────────────────────────────────────────────────────

CAREER_PROFILES = {
    "Software Development Engineer": {
        "required_skills": ["DSA", "System Design", "Java", "Python", "Git", "REST APIs", "SQL"],
        "weight_skill": 0.60,
        "weight_cgpa":  0.20,
        "weight_lc":    0.10,
        "weight_gh":    0.10,
        "avg_salary":   "₹8–35 LPA",
        "demand_trend": "Very High ↑",
    },
    "Data Scientist / ML Engineer": {
        "required_skills": ["Python", "Machine Learning", "Deep Learning", "Statistics", "SQL", "Data Analysis"],
        "weight_skill": 0.60,
        "weight_cgpa":  0.25,
        "weight_lc":    0.05,
        "weight_gh":    0.10,
        "avg_salary":   "₹10–45 LPA",
        "demand_trend": "High ↑",
    },
    "Cloud / DevOps Engineer": {
        "required_skills": ["AWS", "Docker", "Kubernetes", "Linux", "Git", "Python", "Networking"],
        "weight_skill": 0.60,
        "weight_cgpa":  0.15,
        "weight_lc":    0.05,
        "weight_gh":    0.20,
        "avg_salary":   "₹9–40 LPA",
        "demand_trend": "High ↑",
    },
    "Cybersecurity Engineer": {
        "required_skills": ["Networking", "Linux", "Ethical Hacking", "Python", "Git", "SQL"],
        "weight_skill": 0.65,
        "weight_cgpa":  0.15,
        "weight_lc":    0.05,
        "weight_gh":    0.15,
        "avg_salary":   "₹8–32 LPA",
        "demand_trend": "Growing ↑",
    },
    "Product Manager (Tech)": {
        "required_skills": ["Excel", "Figma", "SQL", "REST APIs", "Statistics"],
        "weight_skill": 0.50,
        "weight_cgpa":  0.20,
        "weight_lc":    0.10,
        "weight_gh":    0.20,
        "avg_salary":   "₹12–50 LPA",
        "demand_trend": "Moderate →",
    },
}


# ── SCORING ENGINE ────────────────────────────────────────────────────────────

def normalize(value: float, max_value: float) -> float:
    """Clamp a value to [0, 1]."""
    return min(value / max_value, 1.0) if max_value > 0 else 0.0


def score_career(career_name: str, profile: dict, student: dict) -> float:
    """
    Returns a match score 0–100 for one career.

    student dict keys:
        skills   : list[str]
        cgpa     : float  (0–10)
        leetcode : int    (problems solved)
        github   : int    (repos)
    """
    required = set(profile["required_skills"])
    user_sk  = set(student.get("skills", []))

    skill_overlap = len(required & user_sk) / len(required)
    cgpa_norm     = normalize(student.get("cgpa",    0), 10)
    lc_norm       = normalize(student.get("leetcode",0), 300)
    gh_norm       = normalize(student.get("github",  0), 15)

    raw = (
        profile["weight_skill"] * skill_overlap +
        profile["weight_cgpa"]  * cgpa_norm     +
        profile["weight_lc"]    * lc_norm       +
        profile["weight_gh"]    * gh_norm
    )

    # Map raw 0-1 score → 18-98 display range so no one gets 0
    display_score = round(18 + raw * 80)
    return min(display_score, 98)


def recommend(student: dict) -> list[dict]:
    """Return sorted list of career recommendations."""
    results = []
    for name, profile in CAREER_PROFILES.items():
        sc = score_career(name, profile, student)
        have    = [s for s in student["skills"] if s in profile["required_skills"]]
        missing = [s for s in profile["required_skills"] if s not in student["skills"]]
        results.append({
            "career":       name,
            "score":        sc,
            "skills_have":  have,
            "skills_missing": missing,
            "avg_salary":   profile["avg_salary"],
            "demand_trend": profile["demand_trend"],
        })
    return sorted(results, key=lambda x: x["score"], reverse=True)


def skill_gap_report(student: dict) -> None:
    """Pretty-print the full skill gap report."""
    ranked = recommend(student)
    print("\n" + "═"*55)
    print("  🎯  CAREER PATH RECOMMENDATION REPORT")
    print("═"*55)
    print(f"  Student : {student.get('name','Anonymous')}")
    print(f"  Branch  : {student.get('branch','N/A')}")
    print(f"  CGPA    : {student.get('cgpa', 'N/A')}")
    print(f"  Skills  : {', '.join(student['skills']) or 'None listed'}")
    print("═"*55)

    for rank, r in enumerate(ranked, 1):
        bar = "█" * (r["score"] // 10) + "░" * (10 - r["score"] // 10)
        print(f"\n  #{rank}  {r['career']}")
        print(f"       Match  : [{bar}] {r['score']}%")
        print(f"       Salary : {r['avg_salary']}")
        print(f"       Demand : {r['demand_trend']}")
        if r["skills_have"]:
            print(f"       ✅ Have : {', '.join(r['skills_have'])}")
        if r["skills_missing"]:
            print(f"       ❌ Need : {', '.join(r['skills_missing'])}")

    print("\n" + "═"*55)
    top = ranked[0]
    print(f"\n  🏆  Best Fit → {top['career']} ({top['score']}% match)")
    print(f"  💡  Learn:    {', '.join(top['skills_missing'][:3]) or 'You are well-prepared!'}")
    print("═"*55 + "\n")


# ── DEMO RUN ──────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    sample_student = {
        "name":     "Arjun Verma",
        "branch":   "Computer Science Engineering",
        "cgpa":     8.2,
        "leetcode": 120,
        "github":   6,
        "skills":   ["Python","JavaScript","React","Git","SQL","DSA","HTML/CSS","Node.js"]
    }
    skill_gap_report(sample_student)
