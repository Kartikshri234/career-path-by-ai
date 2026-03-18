"""
career_matcher.py
─────────────────
Core scoring engine for CareerCompass (Django version).
Ported from the original pure-Python scoring module.
"""

# ── CAREER DATA ────────────────────────────────────────────────────────────────

CAREER_PROFILES = {
    "Software Development Engineer": {
        "required_skills": ["DSA", "System Design", "Java", "Python", "Git", "REST APIs", "SQL"],
        "weight_skill": 0.60,
        "weight_cgpa":  0.20,
        "weight_lc":    0.10,
        "weight_gh":    0.10,
        "avg_salary":   "₹8–35 LPA",
        "demand_trend": "Very High ↑",
        "icon":         "💻",
        "desc":         "Build scalable applications and systems. Highest demand across all sectors.",
    },
    "Data Scientist / ML Engineer": {
        "required_skills": ["Python", "Machine Learning", "Deep Learning", "Statistics", "SQL", "Data Analysis", "Power BI"],
        "weight_skill": 0.60,
        "weight_cgpa":  0.25,
        "weight_lc":    0.05,
        "weight_gh":    0.10,
        "avg_salary":   "₹10–45 LPA",
        "demand_trend": "High ↑",
        "icon":         "🤖",
        "desc":         "Extract insights and build intelligent models from large datasets.",
    },
    "Cloud / DevOps Engineer": {
        "required_skills": ["AWS", "Docker", "Kubernetes", "Linux", "Git", "Python", "Networking"],
        "weight_skill": 0.60,
        "weight_cgpa":  0.15,
        "weight_lc":    0.05,
        "weight_gh":    0.20,
        "avg_salary":   "₹9–40 LPA",
        "demand_trend": "High ↑",
        "icon":         "☁️",
        "desc":         "Build cloud infrastructure, CI/CD pipelines, and a strong DevOps culture.",
    },
    "Cybersecurity Engineer": {
        "required_skills": ["Networking", "Linux", "Ethical Hacking", "Python", "Git", "SQL"],
        "weight_skill": 0.65,
        "weight_cgpa":  0.15,
        "weight_lc":    0.05,
        "weight_gh":    0.15,
        "avg_salary":   "₹8–32 LPA",
        "demand_trend": "Growing ↑",
        "icon":         "🔐",
        "desc":         "Protect systems and networks. One of the fastest growing fields in tech.",
    },
    "Product Manager (Tech)": {
        "required_skills": ["Excel", "Figma", "SQL", "REST APIs", "Statistics"],
        "weight_skill": 0.50,
        "weight_cgpa":  0.20,
        "weight_lc":    0.10,
        "weight_gh":    0.20,
        "avg_salary":   "₹12–50 LPA",
        "demand_trend": "Moderate →",
        "icon":         "📋",
        "desc":         "Bridge business and technology. Lead product vision and roadmap.",
    },
}

ROADMAPS = {
    "Software Development Engineer": [
        {"week": "Week 1–2",   "title": "DSA Fundamentals",      "desc": "Arrays, Strings, Linked Lists on LeetCode. Aim for 30+ easy problems.",  "resources": ["LeetCode", "GeeksForGeeks", "Striver SDE Sheet"]},
        {"week": "Week 3–4",   "title": "Core CS Concepts",       "desc": "OS, DBMS, Computer Networks basics — essential for all tech interviews.", "resources": ["Gate Smashers", "YouTube"]},
        {"week": "Week 5–7",   "title": "Full-Stack Project",     "desc": "Build a CRUD app with React + Node.js + MongoDB, deploy on Vercel.",     "resources": ["Traversy Media", "The Odin Project"]},
        {"week": "Week 8–10",  "title": "System Design Basics",   "desc": "Scalability, load balancing, caching, and database design patterns.",    "resources": ["ByteByteGo", "Grokking SD"]},
        {"week": "Week 11–12", "title": "Mock Interviews & Apply","desc": "Do 5+ mock interviews. Apply to 20+ companies simultaneously.",          "resources": ["Pramp", "InterviewBit"]},
    ],
    "Data Scientist / ML Engineer": [
        {"week": "Week 1–2",   "title": "Python & Statistics",    "desc": "NumPy, Pandas, Matplotlib. Descriptive stats and probability.",           "resources": ["Kaggle Learn", "CS50P"]},
        {"week": "Week 3–5",   "title": "ML Core",                "desc": "Regression, Classification, Clustering with Scikit-learn.",               "resources": ["Andrew Ng ML", "Hands-On ML Book"]},
        {"week": "Week 6–8",   "title": "Deep Learning & NLP",    "desc": "Neural nets, CNNs, Transformers basics with PyTorch.",                    "resources": ["Fast.ai", "d2l.ai"]},
        {"week": "Week 9–10",  "title": "Kaggle Competitions",    "desc": "Participate in 2 competitions, focus on feature engineering.",            "resources": ["Kaggle", "Towards Data Science"]},
        {"week": "Week 11–12", "title": "End-to-End ML Project",  "desc": "Build, deploy and document a complete ML pipeline on the cloud.",         "resources": ["MLflow", "Streamlit", "HuggingFace"]},
    ],
    "Cloud / DevOps Engineer": [
        {"week": "Week 1–2",   "title": "Linux & Networking",          "desc": "Shell scripting, TCP/IP, DNS. Practice on Linux VMs.",                      "resources": ["Linux Journey", "NetworkChuck"]},
        {"week": "Week 3–4",   "title": "Docker & Containers",         "desc": "Containerize apps, write Dockerfiles, use Docker Compose.",                  "resources": ["Docker Docs", "TechWorld Nana"]},
        {"week": "Week 5–7",   "title": "AWS Fundamentals",            "desc": "EC2, S3, RDS, VPC, IAM. Prep for AWS Solutions Architect cert.",             "resources": ["Adrian Cantrill", "AWS Free Tier"]},
        {"week": "Week 8–10",  "title": "Kubernetes & CI/CD",          "desc": "K8s deployments, GitHub Actions, Jenkins pipelines.",                        "resources": ["K8s Docs", "DevOps Mumshad"]},
        {"week": "Week 11–12", "title": "Certify & Build Portfolio",   "desc": "Get AWS SAA cert. Deploy a 3-tier app with full CI/CD.",                     "resources": ["ExamPro", "Udemy"]},
    ],
    "Cybersecurity Engineer": [
        {"week": "Week 1–2",   "title": "Networking Fundamentals", "desc": "OSI model, TCP/IP, DNS, firewalls. TryHackMe beginner rooms.",                  "resources": ["TryHackMe", "CompTIA Net+"]},
        {"week": "Week 3–4",   "title": "Linux & Bash Scripting",   "desc": "File permissions, cron, log analysis. Automate tasks in Bash.",                 "resources": ["OverTheWire", "Linux Journey"]},
        {"week": "Week 5–7",   "title": "Ethical Hacking Basics",   "desc": "Reconnaissance, vulnerability scanning, Metasploit intro.",                    "resources": ["Hack The Box", "TCM Security"]},
        {"week": "Week 8–10",  "title": "Web App Security",          "desc": "OWASP Top 10, SQL injection, XSS, Burp Suite.",                                "resources": ["PortSwigger Academy", "OWASP"]},
        {"week": "Week 11–12", "title": "Certify & CTF Practice",    "desc": "Attempt CEH or CompTIA Security+. Join CTF competitions.",                     "resources": ["CTFtime.org", "TryHackMe"]},
    ],
    "Product Manager (Tech)": [
        {"week": "Week 1–2",   "title": "PM Fundamentals",        "desc": "Product thinking, user stories, roadmaps. Read 'Inspired' by Marty Cagan.",    "resources": ["Lenny's Newsletter", "Product School"]},
        {"week": "Week 3–4",   "title": "SQL & Data Analysis",    "desc": "Write real SQL queries. Understand A/B testing and metrics.",                   "resources": ["Mode Analytics", "DataLemur"]},
        {"week": "Week 5–7",   "title": "Figma & UX Basics",      "desc": "Design wireframes and prototypes. Understand UX research methods.",             "resources": ["Figma Tutorials", "NNGroup"]},
        {"week": "Week 8–10",  "title": "Product Case Studies",   "desc": "Analyze 10 product teardowns. Practice estimation + product sense.",            "resources": ["Exponent", "Product Alliance"]},
        {"week": "Week 11–12", "title": "PM Interviews & Apply",  "desc": "Mock PM interviews. Apply to APM programs and PM internships.",                 "resources": ["Exponent", "Glassdoor"]},
    ],
}

SALARY_DATA = {
    "Software Development Engineer": [
        {"city": "Bangalore", "range": "₹8–35 LPA",  "exp": "0–5 yrs"},
        {"city": "Hyderabad", "range": "₹7–28 LPA",  "exp": "0–5 yrs"},
        {"city": "Pune",      "range": "₹6–22 LPA",  "exp": "0–5 yrs"},
        {"city": "Mumbai",    "range": "₹9–40 LPA",  "exp": "0–5 yrs"},
        {"city": "Chennai",   "range": "₹6–20 LPA",  "exp": "0–5 yrs"},
        {"city": "Remote",    "range": "₹12–60 LPA", "exp": "2+ yrs"},
    ],
    "Data Scientist / ML Engineer": [
        {"city": "Bangalore", "range": "₹10–45 LPA", "exp": "0–5 yrs"},
        {"city": "Hyderabad", "range": "₹9–35 LPA",  "exp": "0–5 yrs"},
        {"city": "Mumbai",    "range": "₹11–50 LPA", "exp": "0–5 yrs"},
        {"city": "Pune",      "range": "₹8–30 LPA",  "exp": "0–5 yrs"},
        {"city": "Delhi NCR", "range": "₹9–38 LPA",  "exp": "0–5 yrs"},
        {"city": "Remote US", "range": "$80–150K",    "exp": "2+ yrs"},
    ],
    "Cloud / DevOps Engineer": [
        {"city": "Bangalore", "range": "₹9–40 LPA",  "exp": "0–5 yrs"},
        {"city": "Hyderabad", "range": "₹8–32 LPA",  "exp": "0–5 yrs"},
        {"city": "Pune",      "range": "₹7–28 LPA",  "exp": "0–5 yrs"},
        {"city": "Mumbai",    "range": "₹10–45 LPA", "exp": "0–5 yrs"},
        {"city": "Chennai",   "range": "₹7–25 LPA",  "exp": "0–5 yrs"},
        {"city": "Remote",    "range": "₹15–70 LPA", "exp": "3+ yrs"},
    ],
    "Cybersecurity Engineer": [
        {"city": "Bangalore", "range": "₹8–32 LPA",  "exp": "0–5 yrs"},
        {"city": "Hyderabad", "range": "₹7–28 LPA",  "exp": "0–5 yrs"},
        {"city": "Mumbai",    "range": "₹9–35 LPA",  "exp": "0–5 yrs"},
        {"city": "Pune",      "range": "₹7–25 LPA",  "exp": "0–5 yrs"},
        {"city": "Delhi NCR", "range": "₹8–30 LPA",  "exp": "0–5 yrs"},
        {"city": "Remote",    "range": "₹12–55 LPA", "exp": "2+ yrs"},
    ],
    "Product Manager (Tech)": [
        {"city": "Bangalore", "range": "₹12–50 LPA", "exp": "0–5 yrs"},
        {"city": "Mumbai",    "range": "₹13–55 LPA", "exp": "0–5 yrs"},
        {"city": "Delhi NCR", "range": "₹11–45 LPA", "exp": "0–5 yrs"},
        {"city": "Hyderabad", "range": "₹10–40 LPA", "exp": "0–5 yrs"},
        {"city": "Pune",      "range": "₹9–35 LPA",  "exp": "0–5 yrs"},
        {"city": "Remote US", "range": "$100–180K",   "exp": "3+ yrs"},
    ],
}

ALL_SKILLS = [
    "Python", "Java", "C++", "JavaScript", "SQL", "HTML/CSS", "React", "Node.js",
    "Machine Learning", "Deep Learning", "Data Analysis", "Statistics",
    "Docker", "Kubernetes", "AWS", "Git", "Linux", "Networking",
    "DSA", "System Design", "Figma", "MongoDB", "REST APIs",
    "R", "MATLAB", "Ethical Hacking", "Microcontrollers", "Excel", "Power BI",
]


# ── SCORING ENGINE ─────────────────────────────────────────────────────────────

def _normalize(value: float, max_value: float) -> float:
    return min(value / max_value, 1.0) if max_value > 0 else 0.0


def _score_career(profile: dict, student: dict) -> int:
    required = set(profile["required_skills"])
    user_sk  = set(student.get("skills", []))

    skill_overlap = len(required & user_sk) / len(required) if required else 0
    cgpa_norm     = _normalize(student.get("cgpa",    0), 10)
    lc_norm       = _normalize(student.get("leetcode", 0), 300)
    gh_norm       = _normalize(student.get("github",   0), 15)

    raw = (
        profile["weight_skill"] * skill_overlap +
        profile["weight_cgpa"]  * cgpa_norm     +
        profile["weight_lc"]    * lc_norm       +
        profile["weight_gh"]    * gh_norm
    )
    return min(round(18 + raw * 80), 98)


def _score_breakdown(profile: dict, student: dict) -> dict:
    """Return individual component contributions (in score points, out of 100)."""
    required = set(profile["required_skills"])
    user_sk  = set(student.get("skills", []))
    skill_overlap = len(required & user_sk) / len(required) if required else 0
    cgpa_norm     = _normalize(student.get("cgpa",     0), 10)
    lc_norm       = _normalize(student.get("leetcode", 0), 300)
    gh_norm       = _normalize(student.get("github",   0), 15)

    skill_pts = round(profile["weight_skill"] * skill_overlap * 80)
    cgpa_pts  = round(profile["weight_cgpa"]  * cgpa_norm    * 80)
    lc_pts    = round(profile["weight_lc"]    * lc_norm      * 80)
    gh_pts    = round(profile["weight_gh"]    * gh_norm      * 80)

    return {
        "skill_pts":    skill_pts,
        "cgpa_pts":     cgpa_pts,
        "lc_pts":       lc_pts,
        "gh_pts":       gh_pts,
        "base_pts":     18,
        "skill_pct":    round(len(required & user_sk) / len(required) * 100) if required else 0,
        "cgpa_pct":     round(cgpa_norm * 100),
        "lc_pct":       round(lc_norm   * 100),
        "gh_pct":       round(gh_norm   * 100),
        "skill_weight": round(profile["weight_skill"] * 100),
        "cgpa_weight":  round(profile["weight_cgpa"]  * 100),
        "lc_weight":    round(profile["weight_lc"]    * 100),
        "gh_weight":    round(profile["weight_gh"]    * 100),
    }


def recommend(student: dict) -> list:
    """
    Given a student dict with keys: name, branch, cgpa, leetcode, github, skills
    Returns a list of dicts sorted by score descending.
    """
    results = []
    for name, profile in CAREER_PROFILES.items():
        sc        = _score_career(profile, student)
        breakdown = _score_breakdown(profile, student)
        have    = [s for s in student["skills"] if s in profile["required_skills"]]
        missing = [s for s in profile["required_skills"] if s not in student["skills"]]
        results.append({
            "career":          name,
            "score":           sc,
            "breakdown":       breakdown,
            "skills_have":     have,
            "skills_missing":  missing,
            "avg_salary":      profile["avg_salary"],
            "demand_trend":    profile["demand_trend"],
            "icon":            profile["icon"],
            "desc":            profile["desc"],
            "roadmap":         ROADMAPS.get(name, []),
            "salary":          SALARY_DATA.get(name, []),
        })
    return sorted(results, key=lambda x: x["score"], reverse=True)
