"""
career_engine.py
Core scoring engine — upgraded from career_matcher.py
"""

SKILLS_LIST = [
    "Python", "Java", "C++", "JavaScript", "SQL", "HTML/CSS", "React", "Node.js",
    "Machine Learning", "Deep Learning", "Data Analysis", "Statistics",
    "Docker", "Kubernetes", "AWS", "Git", "Linux", "Networking",
    "DSA", "System Design", "Figma", "MongoDB", "REST APIs",
    "R", "MATLAB", "Ethical Hacking", "Microcontrollers", "Excel", "Power BI"
]

CAREER_PROFILES = {
    "Software Development Engineer": {
        "icon": "💻",
        "desc": "Build scalable applications and systems. Highest demand across all sectors.",
        "required_skills": ["DSA", "System Design", "Java", "Python", "Git", "REST APIs", "SQL"],
        "weight_skill": 0.60, "weight_cgpa": 0.20, "weight_lc": 0.10, "weight_gh": 0.10,
        "weight_skill_pct": 60, "weight_cgpa_pct": 20, "weight_lc_pct": 10, "weight_gh_pct": 10,
        "avg_salary": "₹8–35 LPA", "demand_trend": "Very High ↑", "demand_level": "very_high",
        "salary_level": "high",
        "difficulty": "Medium",
        "time_to_ready": "6–12 months",
        "job_roles": ["Backend Engineer", "Frontend Engineer", "Full-Stack Dev", "SDE-1 / SDE-2", "Software Architect"],
        "top_companies": ["Google", "Amazon", "Microsoft", "Flipkart", "Paytm", "Swiggy", "Razorpay"],
        "certifications": ["AWS Developer", "Oracle Java Certified", "Google Cloud Dev"],
        "day_in_life": "Write and review code, attend standups, debug issues, collaborate with designers and PMs to ship features.",
        "growth_path": "SDE-1 → SDE-2 → Senior SDE → Staff Engineer → Principal / EM",
        "growth_steps": ["SDE-1", "SDE-2", "Senior SDE", "Staff Engineer", "Principal / EM"],
        "radar_labels": ["Coding", "System Design", "CS Basics", "Problem Solving", "Communication", "Projects"],
        "radar_required": [9, 7, 8, 9, 6, 7],
        "roadmap": [
            {"week": "Week 1–2",   "title": "DSA Fundamentals",      "desc": "Arrays, Strings, Linked Lists on LeetCode. Aim for 30+ easy problems.",           "resources": ["LeetCode", "GeeksForGeeks", "Striver SDE Sheet"]},
            {"week": "Week 3–4",   "title": "Core CS Concepts",       "desc": "OS, DBMS, Computer Networks basics — essential for all tech interviews.",          "resources": ["Gate Smashers", "YouTube"]},
            {"week": "Week 5–7",   "title": "Full-Stack Project",     "desc": "Build a CRUD app with React + Node.js + MongoDB, deploy on Vercel.",               "resources": ["Traversy Media", "The Odin Project"]},
            {"week": "Week 8–10",  "title": "System Design Basics",   "desc": "Scalability, load balancing, caching, and database design patterns.",              "resources": ["ByteByteGo", "Grokking SD"]},
            {"week": "Week 11–12", "title": "Mock Interviews & Apply","desc": "Do 5+ mock interviews. Apply to 20+ companies simultaneously.",                     "resources": ["Pramp", "InterviewBit"]},
        ],
        "salary": [
            {"city": "Bangalore", "range": "₹8–35 LPA",  "exp": "0–5 yrs"},
            {"city": "Hyderabad", "range": "₹7–28 LPA",  "exp": "0–5 yrs"},
            {"city": "Pune",      "range": "₹6–22 LPA",  "exp": "0–5 yrs"},
            {"city": "Mumbai",    "range": "₹9–40 LPA",  "exp": "0–5 yrs"},
            {"city": "Chennai",   "range": "₹6–20 LPA",  "exp": "0–5 yrs"},
            {"city": "Remote",    "range": "₹12–60 LPA", "exp": "2+ yrs"},
        ],
    },
    "Data Scientist / ML Engineer": {
        "icon": "🤖",
        "desc": "Extract insights and build intelligent models from large datasets.",
        "required_skills": ["Python", "Machine Learning", "Deep Learning", "Statistics", "SQL", "Data Analysis", "Power BI"],
        "weight_skill": 0.60, "weight_cgpa": 0.25, "weight_lc": 0.05, "weight_gh": 0.10,
        "weight_skill_pct": 60, "weight_cgpa_pct": 25, "weight_lc_pct": 5, "weight_gh_pct": 10,
        "avg_salary": "₹10–45 LPA", "demand_trend": "High ↑", "demand_level": "high",
        "salary_level": "very_high",
        "difficulty": "Hard",
        "time_to_ready": "8–14 months",
        "job_roles": ["Data Scientist", "ML Engineer", "AI Researcher", "Data Analyst", "MLOps Engineer"],
        "top_companies": ["Google DeepMind", "Meta AI", "Amazon", "Flipkart", "CRED", "Meesho", "Fractal"],
        "certifications": ["TensorFlow Developer", "AWS ML Specialty", "Databricks ML Assoc."],
        "day_in_life": "Explore datasets, build and tune models, collaborate with data engineers, present insights to stakeholders.",
        "growth_path": "Data Analyst → Junior DS → Senior DS → Lead DS → Head of AI",
        "growth_steps": ["Data Analyst", "Junior DS", "Senior DS", "Lead DS", "Head of AI"],
        "radar_labels": ["Python", "Statistics", "ML Knowledge", "Data Viz", "Research", "Problem Solving"],
        "radar_required": [9, 8, 9, 7, 8, 8],
        "roadmap": [
            {"week": "Week 1–2",   "title": "Python & Statistics",   "desc": "NumPy, Pandas, Matplotlib. Descriptive stats and probability.",                     "resources": ["Kaggle Learn", "CS50P"]},
            {"week": "Week 3–5",   "title": "ML Core",               "desc": "Regression, Classification, Clustering with Scikit-learn.",                        "resources": ["Andrew Ng ML", "Hands-On ML Book"]},
            {"week": "Week 6–8",   "title": "Deep Learning & NLP",   "desc": "Neural nets, CNNs, Transformers basics with PyTorch.",                             "resources": ["Fast.ai", "d2l.ai"]},
            {"week": "Week 9–10",  "title": "Kaggle Competitions",   "desc": "Participate in 2 competitions, focus on feature engineering.",                     "resources": ["Kaggle", "Towards Data Science"]},
            {"week": "Week 11–12", "title": "End-to-End ML Project", "desc": "Build, deploy and document a complete ML pipeline on the cloud.",                  "resources": ["MLflow", "Streamlit", "HuggingFace"]},
        ],
        "salary": [
            {"city": "Bangalore", "range": "₹10–45 LPA", "exp": "0–5 yrs"},
            {"city": "Hyderabad", "range": "₹9–35 LPA",  "exp": "0–5 yrs"},
            {"city": "Mumbai",    "range": "₹11–50 LPA", "exp": "0–5 yrs"},
            {"city": "Pune",      "range": "₹8–30 LPA",  "exp": "0–5 yrs"},
            {"city": "Delhi NCR", "range": "₹9–38 LPA",  "exp": "0–5 yrs"},
            {"city": "Remote US", "range": "$80–150K",   "exp": "2+ yrs"},
        ],
    },
    "Cloud / DevOps Engineer": {
        "icon": "☁️",
        "desc": "Build cloud infrastructure, CI/CD pipelines, and a strong DevOps culture.",
        "required_skills": ["AWS", "Docker", "Kubernetes", "Linux", "Git", "Python", "Networking"],
        "weight_skill": 0.60, "weight_cgpa": 0.15, "weight_lc": 0.05, "weight_gh": 0.20,
        "weight_skill_pct": 60, "weight_cgpa_pct": 15, "weight_lc_pct": 5, "weight_gh_pct": 20,
        "avg_salary": "₹9–40 LPA", "demand_trend": "High ↑", "demand_level": "high",
        "salary_level": "high",
        "difficulty": "Medium",
        "time_to_ready": "6–10 months",
        "job_roles": ["DevOps Engineer", "Cloud Engineer", "SRE", "Platform Engineer", "Infrastructure Lead"],
        "top_companies": ["Amazon AWS", "Google Cloud", "Infosys", "TCS", "Razorpay", "Zepto", "PhonePe"],
        "certifications": ["AWS Solutions Architect", "CKA (Kubernetes)", "GCP Professional"],
        "day_in_life": "Manage CI/CD pipelines, monitor infrastructure, automate deployments, ensure uptime and security of cloud systems.",
        "growth_path": "Jr DevOps → DevOps Eng → Sr DevOps → Cloud Architect → VP Infra",
        "growth_steps": ["Jr DevOps", "DevOps Eng", "Sr DevOps", "Cloud Architect", "VP Infra"],
        "radar_labels": ["Linux", "Cloud Platforms", "Scripting", "Networking", "CI/CD", "Security"],
        "radar_required": [8, 9, 7, 8, 8, 7],
        "roadmap": [
            {"week": "Week 1–2",   "title": "Linux & Networking",       "desc": "Shell scripting, TCP/IP, DNS. Practice on Linux VMs.",                          "resources": ["Linux Journey", "NetworkChuck"]},
            {"week": "Week 3–4",   "title": "Docker & Containers",      "desc": "Containerize apps, write Dockerfiles, use Docker Compose.",                    "resources": ["Docker Docs", "TechWorld Nana"]},
            {"week": "Week 5–7",   "title": "AWS Fundamentals",         "desc": "EC2, S3, RDS, VPC, IAM. Prep for AWS Solutions Architect cert.",               "resources": ["Adrian Cantrill", "AWS Free Tier"]},
            {"week": "Week 8–10",  "title": "Kubernetes & CI/CD",       "desc": "K8s deployments, GitHub Actions, Jenkins pipelines.",                          "resources": ["K8s Docs", "DevOps Mumshad"]},
            {"week": "Week 11–12", "title": "Certify & Build Portfolio","desc": "Get AWS SAA cert. Deploy a 3-tier app with full CI/CD.",                       "resources": ["ExamPro", "Udemy"]},
        ],
        "salary": [
            {"city": "Bangalore", "range": "₹9–40 LPA",  "exp": "0–5 yrs"},
            {"city": "Hyderabad", "range": "₹8–32 LPA",  "exp": "0–5 yrs"},
            {"city": "Pune",      "range": "₹7–28 LPA",  "exp": "0–5 yrs"},
            {"city": "Mumbai",    "range": "₹10–45 LPA", "exp": "0–5 yrs"},
            {"city": "Chennai",   "range": "₹7–25 LPA",  "exp": "0–5 yrs"},
            {"city": "Remote",    "range": "₹15–70 LPA", "exp": "3+ yrs"},
        ],
    },
    "Cybersecurity Engineer": {
        "icon": "🔐",
        "desc": "Protect systems and networks. One of the fastest growing fields in tech.",
        "required_skills": ["Networking", "Linux", "Ethical Hacking", "Python", "Git", "SQL"],
        "weight_skill": 0.65, "weight_cgpa": 0.15, "weight_lc": 0.05, "weight_gh": 0.15,
        "weight_skill_pct": 65, "weight_cgpa_pct": 15, "weight_lc_pct": 5, "weight_gh_pct": 15,
        "avg_salary": "₹8–32 LPA", "demand_trend": "Growing ↑", "demand_level": "growing",
        "salary_level": "medium",
        "difficulty": "Hard",
        "time_to_ready": "8–12 months",
        "job_roles": ["Penetration Tester", "SOC Analyst", "Security Engineer", "Red Team Lead", "CISO"],
        "top_companies": ["Palo Alto", "CrowdStrike", "IBM Security", "Wipro CyberSec", "HackerOne", "DRDO"],
        "certifications": ["CEH", "CompTIA Security+", "OSCP", "CISSP"],
        "day_in_life": "Run vulnerability scans, analyse security incidents, write penetration test reports, patch systems, monitor SIEM dashboards.",
        "growth_path": "SOC Analyst L1 → Security Engineer → Pen Tester → Red Team Lead → CISO",
        "growth_steps": ["SOC Analyst L1", "Security Engineer", "Pen Tester", "Red Team Lead", "CISO"],
        "radar_labels": ["Networking", "Linux", "Ethical Hacking", "Scripting", "Web Security", "Forensics"],
        "radar_required": [9, 8, 9, 7, 8, 6],
        "roadmap": [
            {"week": "Week 1–2",   "title": "Networking Fundamentals", "desc": "OSI model, TCP/IP, DNS, firewalls. TryHackMe beginner rooms.",                  "resources": ["TryHackMe", "CompTIA Net+"]},
            {"week": "Week 3–4",   "title": "Linux & Bash Scripting",  "desc": "File permissions, cron, log analysis. Automate tasks in Bash.",                "resources": ["OverTheWire", "Linux Journey"]},
            {"week": "Week 5–7",   "title": "Ethical Hacking Basics",  "desc": "Reconnaissance, vulnerability scanning, Metasploit intro.",                    "resources": ["Hack The Box", "TCM Security"]},
            {"week": "Week 8–10",  "title": "Web App Security",        "desc": "OWASP Top 10, SQL injection, XSS, Burp Suite.",                                "resources": ["PortSwigger Academy", "OWASP"]},
            {"week": "Week 11–12", "title": "Certify & CTF Practice",  "desc": "Attempt CEH or CompTIA Security+. Join CTF competitions.",                     "resources": ["CTFtime.org", "TryHackMe"]},
        ],
        "salary": [
            {"city": "Bangalore", "range": "₹8–32 LPA",  "exp": "0–5 yrs"},
            {"city": "Hyderabad", "range": "₹7–28 LPA",  "exp": "0–5 yrs"},
            {"city": "Mumbai",    "range": "₹9–35 LPA",  "exp": "0–5 yrs"},
            {"city": "Pune",      "range": "₹7–25 LPA",  "exp": "0–5 yrs"},
            {"city": "Delhi NCR", "range": "₹8–30 LPA",  "exp": "0–5 yrs"},
            {"city": "Remote",    "range": "₹12–55 LPA", "exp": "2+ yrs"},
        ],
    },
    "Product Manager (Tech)": {
        "icon": "📋",
        "desc": "Drive product strategy and bridge the gap between business and engineering.",
        "required_skills": ["Excel", "Figma", "SQL", "REST APIs", "Statistics"],
        "weight_skill": 0.50, "weight_cgpa": 0.20, "weight_lc": 0.10, "weight_gh": 0.20,
        "weight_skill_pct": 50, "weight_cgpa_pct": 20, "weight_lc_pct": 10, "weight_gh_pct": 20,
        "avg_salary": "₹12–50 LPA", "demand_trend": "Moderate →", "demand_level": "moderate",
        "salary_level": "very_high",
        "difficulty": "Medium",
        "time_to_ready": "4–8 months",
        "job_roles": ["Associate PM", "Product Manager", "Senior PM", "Group PM", "VP of Product"],
        "top_companies": ["Google", "Microsoft", "Meesho", "Swiggy", "Razorpay", "Zepto", "CRED"],
        "certifications": ["Product School CPM", "Pragmatic Institute", "Google PM Certificate"],
        "day_in_life": "Write PRDs, run sprint planning, talk to users, analyse metrics, prioritise the roadmap, and align engineering + design.",
        "growth_path": "APM → PM → Sr PM → Group PM → Director of Product → CPO",
        "growth_steps": ["APM", "PM", "Sr PM", "Group PM", "Director of Product", "CPO"],
        "radar_labels": ["Product Thinking", "Data Skills", "Communication", "Technical Knowledge", "Strategy", "Leadership"],
        "radar_required": [9, 7, 9, 6, 8, 8],
        "roadmap": [
            {"week": "Week 1–2",   "title": "PM Fundamentals",         "desc": "Product thinking, PRDs, user stories. Read 'Inspired' by Marty Cagan.",         "resources": ["Lenny's Newsletter", "PM School"]},
            {"week": "Week 3–4",   "title": "Data & Analytics",        "desc": "SQL for product analytics, A/B testing basics, funnel analysis.",               "resources": ["Mode Analytics", "Mixpanel Academy"]},
            {"week": "Week 5–7",   "title": "UX & Figma Prototyping",  "desc": "User research, wireframing, clickable prototypes in Figma.",                    "resources": ["Figma Learn", "Nielsen Norman Group"]},
            {"week": "Week 8–10",  "title": "Strategy & Roadmapping",  "desc": "OKRs, prioritization frameworks (RICE, ICE), competitive analysis.",           "resources": ["ProductPlan", "Roman Pichler"]},
            {"week": "Week 11–12", "title": "Case Studies & Interviews","desc": "Practice product cases. Build a portfolio of 3 case studies.",                 "resources": ["Exponent", "ProductHQ"]},
        ],
        "salary": [
            {"city": "Bangalore", "range": "₹12–50 LPA", "exp": "0–5 yrs"},
            {"city": "Hyderabad", "range": "₹10–40 LPA", "exp": "0–5 yrs"},
            {"city": "Mumbai",    "range": "₹14–55 LPA", "exp": "0–5 yrs"},
            {"city": "Pune",      "range": "₹10–38 LPA", "exp": "0–5 yrs"},
            {"city": "Delhi NCR", "range": "₹12–45 LPA", "exp": "0–5 yrs"},
            {"city": "Remote",    "range": "₹18–80 LPA", "exp": "3+ yrs"},
        ],
    },
}


def normalize(value: float, max_value: float) -> float:
    return min(value / max_value, 1.0) if max_value > 0 else 0.0


def score_career(career_name: str, profile: dict, student: dict) -> float:
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
    return min(round(18 + raw * 80), 98)


def recommend(student: dict) -> list:
    results = []
    for name, profile in CAREER_PROFILES.items():
        sc = score_career(name, profile, student)
        have    = [s for s in student.get("skills", []) if s in profile["required_skills"]]
        missing = [s for s in profile["required_skills"] if s not in student.get("skills", [])]
        results.append({
            "career":         name,
            "icon":           profile["icon"],
            "desc":           profile["desc"],
            "score":          sc,
            "skills_have":    have,
            "skills_missing": missing,
            "avg_salary":     profile["avg_salary"],
            "demand_trend":   profile["demand_trend"],
            "roadmap":        profile["roadmap"],
            "salary":         profile["salary"],
            "radar_labels":   profile["radar_labels"],
            "radar_required": profile["radar_required"],
        })
    return sorted(results, key=lambda x: x["score"], reverse=True)
