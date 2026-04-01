"""
career_engine.py  — v2.0
Expanded to 10 career tracks with city demand intelligence.
"""

SKILLS_LIST = [
    # Core languages
    "Python", "Java", "C++", "JavaScript", "TypeScript", "SQL",
    "HTML/CSS", "Go", "Rust", "Swift", "Kotlin", "R", "MATLAB",
    # Web & mobile
    "React", "Node.js", "Vue.js", "Next.js", "Django", "Flutter",
    # Data & AI
    "Machine Learning", "Deep Learning", "Data Analysis", "Statistics",
    "TensorFlow", "PyTorch", "NLP", "Computer Vision",
    # Infrastructure
    "Docker", "Kubernetes", "AWS", "Azure", "GCP", "Linux",
    "Networking", "Terraform", "CI/CD",
    # Engineering
    "DSA", "System Design", "REST APIs", "GraphQL", "MongoDB",
    "PostgreSQL", "Redis", "Microservices",
    # Design & Product
    "Figma", "UI/UX Design",
    # Security
    "Ethical Hacking", "Penetration Testing", "SIEM",
    # Embedded
    "Microcontrollers", "Arduino", "RTOS",
    # Analytics
    "Excel", "Power BI", "Tableau",
    # Misc
    "Git", "Blockchain", "Smart Contracts", "Solidity",
]

CAREER_PROFILES = {

    # ── 1 ─────────────────────────────────────────
    "Software Development Engineer": {
        "icon": "💻",
        "desc": "Build scalable applications and systems. Highest demand across all sectors.",
        "required_skills": ["DSA", "System Design", "Java", "Python", "Git", "REST APIs", "SQL"],
        "weight_skill": 0.60, "weight_cgpa": 0.20, "weight_lc": 0.10, "weight_gh": 0.10,
        "weight_skill_pct": 60, "weight_cgpa_pct": 20, "weight_lc_pct": 10, "weight_gh_pct": 10,
        "avg_salary": "₹8–35 LPA", "demand_trend": "Very High ↑", "demand_level": "very_high",
        "salary_level": "high", "difficulty": "Medium", "time_to_ready": "6–12 months",
        "job_roles": ["Backend Engineer", "Frontend Engineer", "Full-Stack Dev", "SDE-1 / SDE-2", "Software Architect"],
        "top_companies": ["Google", "Amazon", "Microsoft", "Flipkart", "Paytm", "Swiggy", "Razorpay"],
        "certifications": ["AWS Developer", "Oracle Java Certified", "Google Cloud Dev"],
        "day_in_life": "Write and review code, attend standups, debug issues, collaborate with designers and PMs to ship features.",
        "growth_path": "SDE-1 → SDE-2 → Senior SDE → Staff Engineer → Principal / EM",
        "growth_steps": ["SDE-1", "SDE-2", "Senior SDE", "Staff Engineer", "Principal / EM"],
        "radar_labels": ["Coding", "System Design", "CS Basics", "Problem Solving", "Communication", "Projects"],
        "radar_required": [9, 7, 8, 9, 6, 7],
        "city_demand": [
            {"city": "Bangalore",  "demand": "🔥 Highest",  "openings": "12,000+", "why": "Silicon Valley of India — Google, Flipkart, Amazon, 1000+ startups"},
            {"city": "Hyderabad",  "demand": "🔥 Very High","openings": "8,500+",  "why": "Microsoft, Amazon, Infosys campuses, Telangana startup boom"},
            {"city": "Pune",       "demand": "📈 High",      "openings": "6,000+",  "why": "Tier-2 tech hub, lower cost of living, major IT parks"},
            {"city": "Mumbai",     "demand": "📈 High",      "openings": "5,500+",  "why": "Fintech and media companies, Navi Mumbai tech zone"},
            {"city": "Delhi NCR",  "demand": "📈 High",      "openings": "5,000+",  "why": "Gurugram startups, Noida IT hub, government digital projects"},
            {"city": "Chennai",    "demand": "📊 Moderate",  "openings": "3,500+",  "why": "Zoho, Freshworks HQ, strong MNC presence"},
        ],
        "roadmap": [
            {"week": "Week 1–2",   "title": "DSA Fundamentals",       "desc": "Arrays, Strings, Linked Lists on LeetCode. Aim for 30+ easy problems.",          "resources": ["LeetCode", "GeeksForGeeks", "Striver SDE Sheet"]},
            {"week": "Week 3–4",   "title": "Core CS Concepts",        "desc": "OS, DBMS, Computer Networks basics — essential for all tech interviews.",         "resources": ["Gate Smashers", "YouTube"]},
            {"week": "Week 5–7",   "title": "Full-Stack Project",      "desc": "Build a CRUD app with React + Node.js + MongoDB, deploy on Vercel.",              "resources": ["Traversy Media", "The Odin Project"]},
            {"week": "Week 8–10",  "title": "System Design Basics",    "desc": "Scalability, load balancing, caching, and database design patterns.",             "resources": ["ByteByteGo", "Grokking SD"]},
            {"week": "Week 11–12", "title": "Mock Interviews & Apply", "desc": "Do 5+ mock interviews. Apply to 20+ companies simultaneously.",                    "resources": ["Pramp", "InterviewBit"]},
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

    # ── 2 ─────────────────────────────────────────
    "Data Scientist / ML Engineer": {
        "icon": "🤖",
        "desc": "Extract insights and build intelligent models from large datasets.",
        "required_skills": ["Python", "Machine Learning", "Deep Learning", "Statistics", "SQL", "Data Analysis", "Power BI"],
        "weight_skill": 0.60, "weight_cgpa": 0.25, "weight_lc": 0.05, "weight_gh": 0.10,
        "weight_skill_pct": 60, "weight_cgpa_pct": 25, "weight_lc_pct": 5, "weight_gh_pct": 10,
        "avg_salary": "₹10–45 LPA", "demand_trend": "High ↑", "demand_level": "high",
        "salary_level": "very_high", "difficulty": "Hard", "time_to_ready": "8–14 months",
        "job_roles": ["Data Scientist", "ML Engineer", "AI Researcher", "Data Analyst", "MLOps Engineer"],
        "top_companies": ["Google DeepMind", "Meta AI", "Amazon", "Flipkart", "CRED", "Meesho", "Fractal"],
        "certifications": ["TensorFlow Developer", "AWS ML Specialty", "Databricks ML Assoc."],
        "day_in_life": "Explore datasets, build and tune models, collaborate with data engineers, present insights to stakeholders.",
        "growth_path": "Data Analyst → Junior DS → Senior DS → Lead DS → Head of AI",
        "growth_steps": ["Data Analyst", "Junior DS", "Senior DS", "Lead DS", "Head of AI"],
        "radar_labels": ["Python", "Statistics", "ML Knowledge", "Data Viz", "Research", "Problem Solving"],
        "radar_required": [9, 8, 9, 7, 8, 8],
        "city_demand": [
            {"city": "Bangalore",  "demand": "🔥 Highest",  "openings": "5,000+", "why": "Global AI R&D hubs for Google, Amazon, Microsoft all based here"},
            {"city": "Hyderabad",  "demand": "🔥 Very High","openings": "3,500+", "why": "Microsoft AI lab, analytics firms, healthcare ML boom"},
            {"city": "Mumbai",     "demand": "📈 High",      "openings": "2,800+", "why": "Fintech ML — risk models, fraud detection, credit scoring"},
            {"city": "Pune",       "demand": "📈 High",      "openings": "2,200+", "why": "Data analytics outsourcing, auto industry AI"},
            {"city": "Delhi NCR",  "demand": "📊 Moderate",  "openings": "2,000+", "why": "EdTech & healthtech AI, government data initiatives"},
            {"city": "Chennai",    "demand": "📊 Moderate",  "openings": "1,500+", "why": "Zoho AI team, manufacturing ML and quality control"},
        ],
        "roadmap": [
            {"week": "Week 1–2",   "title": "Python & Statistics",    "desc": "NumPy, Pandas, Matplotlib. Descriptive stats and probability.",                    "resources": ["Kaggle Learn", "CS50P"]},
            {"week": "Week 3–5",   "title": "ML Core",                "desc": "Regression, Classification, Clustering with Scikit-learn.",                       "resources": ["Andrew Ng ML", "Hands-On ML Book"]},
            {"week": "Week 6–8",   "title": "Deep Learning & NLP",    "desc": "Neural nets, CNNs, Transformers basics with PyTorch.",                            "resources": ["Fast.ai", "d2l.ai"]},
            {"week": "Week 9–10",  "title": "Kaggle Competitions",    "desc": "Participate in 2 competitions, focus on feature engineering.",                    "resources": ["Kaggle", "Towards Data Science"]},
            {"week": "Week 11–12", "title": "End-to-End ML Project",  "desc": "Build, deploy and document a complete ML pipeline on the cloud.",                 "resources": ["MLflow", "Streamlit", "HuggingFace"]},
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

    # ── 3 ─────────────────────────────────────────
    "Cloud / DevOps Engineer": {
        "icon": "☁️",
        "desc": "Build cloud infrastructure, CI/CD pipelines, and a strong DevOps culture.",
        "required_skills": ["AWS", "Docker", "Kubernetes", "Linux", "Git", "Python", "Networking", "CI/CD", "Terraform"],
        "weight_skill": 0.60, "weight_cgpa": 0.15, "weight_lc": 0.05, "weight_gh": 0.20,
        "weight_skill_pct": 60, "weight_cgpa_pct": 15, "weight_lc_pct": 5, "weight_gh_pct": 20,
        "avg_salary": "₹9–40 LPA", "demand_trend": "High ↑", "demand_level": "high",
        "salary_level": "high", "difficulty": "Medium", "time_to_ready": "6–10 months",
        "job_roles": ["DevOps Engineer", "Cloud Engineer", "SRE", "Platform Engineer", "Infrastructure Lead"],
        "top_companies": ["Amazon AWS", "Google Cloud", "Infosys", "TCS", "Razorpay", "Zepto", "PhonePe"],
        "certifications": ["AWS Solutions Architect", "CKA (Kubernetes)", "GCP Professional"],
        "day_in_life": "Manage CI/CD pipelines, monitor infrastructure, automate deployments, ensure uptime and security of cloud systems.",
        "growth_path": "Jr DevOps → DevOps Eng → Sr DevOps → Cloud Architect → VP Infra",
        "growth_steps": ["Jr DevOps", "DevOps Eng", "Sr DevOps", "Cloud Architect", "VP Infra"],
        "radar_labels": ["Linux", "Cloud Platforms", "Scripting", "Networking", "CI/CD", "Security"],
        "radar_required": [8, 9, 7, 8, 8, 7],
        "city_demand": [
            {"city": "Bangalore",  "demand": "🔥 Highest",  "openings": "4,500+", "why": "AWS, GCP, Azure all have large engineering offices here"},
            {"city": "Hyderabad",  "demand": "🔥 Very High","openings": "3,200+", "why": "Microsoft Azure regional HQ, booming SaaS companies"},
            {"city": "Pune",       "demand": "📈 High",      "openings": "2,400+", "why": "IT services transformation to DevOps, automotive tech"},
            {"city": "Mumbai",     "demand": "📈 High",      "openings": "2,200+", "why": "Fintech SRE roles, PhonePe, Zepto, media streaming infra"},
            {"city": "Chennai",    "demand": "📊 Moderate",  "openings": "1,600+", "why": "Zoho DevOps, manufacturing automation, MNC service delivery"},
            {"city": "Delhi NCR",  "demand": "📊 Moderate",  "openings": "1,800+", "why": "Government cloud projects, healthtech infra, EdTech scale-ups"},
        ],
        "roadmap": [
            {"week": "Week 1–2",   "title": "Linux & Networking",        "desc": "Shell scripting, TCP/IP, DNS. Practice on Linux VMs.",                         "resources": ["Linux Journey", "NetworkChuck"]},
            {"week": "Week 3–4",   "title": "Docker & Containers",       "desc": "Containerize apps, write Dockerfiles, use Docker Compose.",                   "resources": ["Docker Docs", "TechWorld Nana"]},
            {"week": "Week 5–7",   "title": "AWS Fundamentals",          "desc": "EC2, S3, RDS, VPC, IAM. Prep for AWS Solutions Architect cert.",              "resources": ["Adrian Cantrill", "AWS Free Tier"]},
            {"week": "Week 8–10",  "title": "Kubernetes & CI/CD",        "desc": "K8s deployments, GitHub Actions, Jenkins pipelines.",                         "resources": ["K8s Docs", "DevOps Mumshad"]},
            {"week": "Week 11–12", "title": "Certify & Build Portfolio", "desc": "Get AWS SAA cert. Deploy a 3-tier app with full CI/CD.",                      "resources": ["ExamPro", "Udemy"]},
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

    # ── 4 ─────────────────────────────────────────
    "Cybersecurity Engineer": {
        "icon": "🔐",
        "desc": "Protect systems and networks. One of the fastest growing fields in tech.",
        "required_skills": ["Networking", "Linux", "Ethical Hacking", "Penetration Testing", "Python", "Git", "SQL", "SIEM"],
        "weight_skill": 0.65, "weight_cgpa": 0.15, "weight_lc": 0.05, "weight_gh": 0.15,
        "weight_skill_pct": 65, "weight_cgpa_pct": 15, "weight_lc_pct": 5, "weight_gh_pct": 15,
        "avg_salary": "₹8–32 LPA", "demand_trend": "Growing ↑", "demand_level": "growing",
        "salary_level": "medium", "difficulty": "Hard", "time_to_ready": "8–12 months",
        "job_roles": ["Penetration Tester", "SOC Analyst", "Security Engineer", "Red Team Lead", "CISO"],
        "top_companies": ["Palo Alto", "CrowdStrike", "IBM Security", "Wipro CyberSec", "HackerOne", "DRDO"],
        "certifications": ["CEH", "CompTIA Security+", "OSCP", "CISSP"],
        "day_in_life": "Run vulnerability scans, analyse security incidents, write penetration test reports, patch systems, monitor SIEM dashboards.",
        "growth_path": "SOC Analyst L1 → Security Engineer → Pen Tester → Red Team Lead → CISO",
        "growth_steps": ["SOC Analyst L1", "Security Engineer", "Pen Tester", "Red Team Lead", "CISO"],
        "radar_labels": ["Networking", "Linux", "Ethical Hacking", "Scripting", "Web Security", "Forensics"],
        "radar_required": [9, 8, 9, 7, 8, 6],
        "city_demand": [
            {"city": "Bangalore",  "demand": "🔥 Very High","openings": "2,800+", "why": "Security teams at Google, Amazon, startups; CERT-In presence"},
            {"city": "Delhi NCR",  "demand": "🔥 Very High","openings": "2,600+", "why": "Government, defence (DRDO, NIC), banking sector security"},
            {"city": "Hyderabad",  "demand": "📈 High",      "openings": "2,000+", "why": "Microsoft security lab, healthcare data compliance"},
            {"city": "Mumbai",     "demand": "📈 High",      "openings": "1,800+", "why": "Banking & financial security (RBI compliance, SEBI regs)"},
            {"city": "Pune",       "demand": "📊 Moderate",  "openings": "1,200+", "why": "IT services security division, BFSI clients"},
            {"city": "Chennai",    "demand": "📊 Moderate",  "openings": "900+",   "why": "MNC security delivery centres, automotive OT security"},
        ],
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

    # ── 5 ─────────────────────────────────────────
    "Product Manager (Tech)": {
        "icon": "📋",
        "desc": "Drive product strategy and bridge the gap between business and engineering.",
        "required_skills": ["Excel", "Figma", "SQL", "REST APIs", "Statistics"],
        "weight_skill": 0.50, "weight_cgpa": 0.20, "weight_lc": 0.10, "weight_gh": 0.20,
        "weight_skill_pct": 50, "weight_cgpa_pct": 20, "weight_lc_pct": 10, "weight_gh_pct": 20,
        "avg_salary": "₹12–50 LPA", "demand_trend": "Moderate →", "demand_level": "moderate",
        "salary_level": "very_high", "difficulty": "Medium", "time_to_ready": "4–8 months",
        "job_roles": ["Associate PM", "Product Manager", "Senior PM", "Group PM", "VP of Product"],
        "top_companies": ["Google", "Microsoft", "Meesho", "Swiggy", "Razorpay", "Zepto", "CRED"],
        "certifications": ["Product School CPM", "Pragmatic Institute", "Google PM Certificate"],
        "day_in_life": "Write PRDs, run sprint planning, talk to users, analyse metrics, prioritise the roadmap, and align engineering + design.",
        "growth_path": "APM → PM → Sr PM → Group PM → Director of Product → CPO",
        "growth_steps": ["APM", "PM", "Sr PM", "Group PM", "Director of Product", "CPO"],
        "radar_labels": ["Product Thinking", "Data Skills", "Communication", "Technical Knowledge", "Strategy", "Leadership"],
        "radar_required": [9, 7, 9, 6, 8, 8],
        "city_demand": [
            {"city": "Bangalore",  "demand": "🔥 Highest",  "openings": "2,200+", "why": "Unicorn startups, consumer internet, B2B SaaS product roles"},
            {"city": "Mumbai",     "demand": "🔥 Very High","openings": "1,800+", "why": "Fintech product, media & entertainment, BFSI digital"},
            {"city": "Delhi NCR",  "demand": "📈 High",      "openings": "1,500+", "why": "EdTech (Byju's, Unacademy), healthtech, D2C e-commerce"},
            {"city": "Hyderabad",  "demand": "📈 High",      "openings": "1,200+", "why": "Microsoft product division, SaaS platforms, IT product companies"},
            {"city": "Pune",       "demand": "📊 Moderate",  "openings": "800+",   "why": "Mid-stage startups, IT product offshoots"},
            {"city": "Chennai",    "demand": "📊 Moderate",  "openings": "600+",   "why": "Zoho product teams, Freshworks APM program"},
        ],
        "roadmap": [
            {"week": "Week 1–2",   "title": "PM Fundamentals",          "desc": "Product thinking, PRDs, user stories. Read 'Inspired' by Marty Cagan.",        "resources": ["Lenny's Newsletter", "PM School"]},
            {"week": "Week 3–4",   "title": "Data & Analytics",         "desc": "SQL for product analytics, A/B testing basics, funnel analysis.",              "resources": ["Mode Analytics", "Mixpanel Academy"]},
            {"week": "Week 5–7",   "title": "UX & Figma Prototyping",   "desc": "User research, wireframing, clickable prototypes in Figma.",                   "resources": ["Figma Learn", "Nielsen Norman Group"]},
            {"week": "Week 8–10",  "title": "Strategy & Roadmapping",   "desc": "OKRs, prioritization frameworks (RICE, ICE), competitive analysis.",          "resources": ["ProductPlan", "Roman Pichler"]},
            {"week": "Week 11–12", "title": "Case Studies & Interviews","desc": "Practice product cases. Build a portfolio of 3 case studies.",                "resources": ["Exponent", "ProductHQ"]},
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

    # ── 6 ─────────────────────────────────────────
    "Full-Stack / Mobile Developer": {
        "icon": "📱",
        "desc": "Build end-to-end web and mobile apps. High freelance and startup demand.",
        "required_skills": ["JavaScript", "TypeScript", "React", "Node.js", "MongoDB", "HTML/CSS", "REST APIs", "Git", "Flutter"],
        "weight_skill": 0.65, "weight_cgpa": 0.10, "weight_lc": 0.10, "weight_gh": 0.15,
        "weight_skill_pct": 65, "weight_cgpa_pct": 10, "weight_lc_pct": 10, "weight_gh_pct": 15,
        "avg_salary": "₹6–30 LPA", "demand_trend": "Very High ↑", "demand_level": "very_high",
        "salary_level": "high", "difficulty": "Medium", "time_to_ready": "5–9 months",
        "job_roles": ["Frontend Developer", "React Native Dev", "Flutter Dev", "Full-Stack Engineer", "Mobile Tech Lead"],
        "top_companies": ["Zomato", "Swiggy", "CRED", "Groww", "Nykaa", "Urban Company", "MakeMyTrip"],
        "certifications": ["Meta React Developer", "Google Flutter Cert", "AWS Amplify"],
        "day_in_life": "Build responsive UIs, write APIs, deploy to app stores, fix bugs, collaborate with designers using Figma specs.",
        "growth_path": "Junior Dev → Mid-Level → Senior Dev → Lead Engineer → CTO",
        "growth_steps": ["Junior Dev", "Mid-Level", "Senior Dev", "Lead Engineer", "CTO"],
        "radar_labels": ["JavaScript/TS", "React/Flutter", "Node.js/API", "CSS/Design", "Mobile", "Git/DevOps"],
        "radar_required": [9, 8, 7, 7, 8, 6],
        "city_demand": [
            {"city": "Bangalore",  "demand": "🔥 Highest",  "openings": "9,000+", "why": "Consumer app startups dominate — Swiggy, CRED, Groww, Zepto"},
            {"city": "Mumbai",     "demand": "🔥 Very High","openings": "5,500+", "why": "Fintech apps, OTT platforms, e-commerce mobile teams"},
            {"city": "Delhi NCR",  "demand": "📈 High",      "openings": "4,500+", "why": "EdTech apps, delivery startups, digital government apps"},
            {"city": "Hyderabad",  "demand": "📈 High",      "openings": "4,000+", "why": "SaaS frontend teams, gaming companies, IT product firms"},
            {"city": "Pune",       "demand": "📈 High",      "openings": "3,200+", "why": "Mid-stage startups, IT services digital transformation"},
            {"city": "Remote",     "demand": "🔥 Very High","openings": "Unlimited", "why": "Highest freelance demand globally — Upwork, Toptal, Fiverr"},
        ],
        "roadmap": [
            {"week": "Week 1–2",   "title": "HTML, CSS & JS Core",      "desc": "Build 3 responsive pages. Learn Flexbox, Grid, and DOM manipulation.",         "resources": ["MDN Web Docs", "Kevin Powell CSS"]},
            {"week": "Week 3–5",   "title": "React & State Management",  "desc": "Build a React app with hooks, React Router, and Redux/Zustand.",               "resources": ["React Docs", "Scrimba"]},
            {"week": "Week 6–8",   "title": "Node.js & REST APIs",       "desc": "Express.js, MongoDB with Mongoose. Build a complete CRUD backend.",            "resources": ["Traversy Media", "The Odin Project"]},
            {"week": "Week 9–10",  "title": "React Native / Flutter",    "desc": "Port your web app to mobile. Deploy to Expo or TestFlight.",                   "resources": ["Flutter Docs", "Academind"]},
            {"week": "Week 11–12", "title": "Deploy & Build Portfolio",  "desc": "Deploy 2 apps publicly. Write case studies. Apply to jobs/freelance.",         "resources": ["Vercel", "Netlify", "GitHub Pages"]},
        ],
        "salary": [
            {"city": "Bangalore", "range": "₹6–30 LPA",  "exp": "0–5 yrs"},
            {"city": "Mumbai",    "range": "₹7–32 LPA",  "exp": "0–5 yrs"},
            {"city": "Delhi NCR", "range": "₹6–28 LPA",  "exp": "0–5 yrs"},
            {"city": "Pune",      "range": "₹5–25 LPA",  "exp": "0–5 yrs"},
            {"city": "Remote IN", "range": "₹8–40 LPA",  "exp": "1+ yrs"},
            {"city": "Remote US", "range": "$60–120K",   "exp": "2+ yrs"},
        ],
    },

    # ── 7 ─────────────────────────────────────────
    "Data / Business Analyst": {
        "icon": "📊",
        "desc": "Turn raw data into business decisions using SQL, Excel and visualisation tools.",
        "required_skills": ["SQL", "Excel", "Power BI", "Tableau", "Python", "Statistics", "Data Analysis"],
        "weight_skill": 0.55, "weight_cgpa": 0.25, "weight_lc": 0.05, "weight_gh": 0.15,
        "weight_skill_pct": 55, "weight_cgpa_pct": 25, "weight_lc_pct": 5, "weight_gh_pct": 15,
        "avg_salary": "₹5–22 LPA", "demand_trend": "High ↑", "demand_level": "high",
        "salary_level": "medium", "difficulty": "Low–Medium", "time_to_ready": "3–6 months",
        "job_roles": ["Business Analyst", "Data Analyst", "BI Developer", "Analytics Engineer", "Strategy Analyst"],
        "top_companies": ["Deloitte", "McKinsey", "Flipkart", "Paytm", "Accenture", "IBM", "Fractal Analytics"],
        "certifications": ["Google Data Analytics", "Power BI PL-300", "Tableau Desktop Specialist"],
        "day_in_life": "Pull data from warehouses, build dashboards, analyse KPIs, present insights to leadership, support product decisions.",
        "growth_path": "Analyst → Sr Analyst → Analytics Manager → Head of Analytics → Chief Data Officer",
        "growth_steps": ["Analyst", "Sr Analyst", "Analytics Manager", "Head of Analytics", "CDO"],
        "radar_labels": ["SQL", "Excel/Sheets", "Power BI/Tableau", "Statistics", "Business Acumen", "Communication"],
        "radar_required": [8, 8, 9, 7, 8, 9],
        "city_demand": [
            {"city": "Bangalore",  "demand": "🔥 Highest",  "openings": "6,500+", "why": "Every tech startup needs analysts — product, growth, finance"},
            {"city": "Mumbai",     "demand": "🔥 Very High","openings": "5,000+", "why": "BFSI analytics boom — banks, AMCs, insurance companies"},
            {"city": "Delhi NCR",  "demand": "📈 High",      "openings": "3,800+", "why": "Consulting firms (Big 4, MBB), EdTech, e-commerce analytics"},
            {"city": "Hyderabad",  "demand": "📈 High",      "openings": "3,200+", "why": "Analytics delivery centres, pharma data, SaaS metrics"},
            {"city": "Pune",       "range": "📊 Moderate",   "openings": "2,200+", "why": "Auto industry analytics, IT services BI teams"},
            {"city": "Chennai",    "demand": "📊 Moderate",  "openings": "1,800+", "why": "Manufacturing analytics, retail data, IT BPO analytics"},
        ],
        "roadmap": [
            {"week": "Week 1–2",   "title": "SQL Foundations",          "desc": "SELECT, JOINs, window functions, subqueries. Practice on Mode/HackerRank.",     "resources": ["SQLZoo", "Mode Analytics"]},
            {"week": "Week 3–4",   "title": "Excel & Google Sheets",    "desc": "PivotTables, VLOOKUP, Power Query, dynamic charts.",                           "resources": ["ExcelJet", "Chandoo.org"]},
            {"week": "Week 5–7",   "title": "Power BI / Tableau",       "desc": "Build 3 dashboards from scratch with real datasets.",                          "resources": ["SQLBI", "Tableau Public"]},
            {"week": "Week 8–9",   "title": "Python for Data Analysis", "desc": "Pandas, Matplotlib, Seaborn for EDA and reporting.",                           "resources": ["Kaggle Learn", "Corey Schafer"]},
            {"week": "Week 10–12", "title": "Case Studies & Portfolio", "desc": "Solve 2 business cases. Build a portfolio on GitHub/Notion.",                  "resources": ["StrataScratch", "Data With Danny"]},
        ],
        "salary": [
            {"city": "Bangalore", "range": "₹5–22 LPA",  "exp": "0–5 yrs"},
            {"city": "Mumbai",    "range": "₹6–24 LPA",  "exp": "0–5 yrs"},
            {"city": "Delhi NCR", "range": "₹5–20 LPA",  "exp": "0–5 yrs"},
            {"city": "Hyderabad", "range": "₹5–18 LPA",  "exp": "0–5 yrs"},
            {"city": "Pune",      "range": "₹4–16 LPA",  "exp": "0–5 yrs"},
            {"city": "Remote",    "range": "₹8–30 LPA",  "exp": "2+ yrs"},
        ],
    },

    # ── 8 ─────────────────────────────────────────
    "UI/UX Designer (Technical)": {
        "icon": "🎨",
        "desc": "Design intuitive, beautiful digital products. Bridge design and engineering.",
        "required_skills": ["Figma", "UI/UX Design", "HTML/CSS", "JavaScript", "Statistics"],
        "weight_skill": 0.60, "weight_cgpa": 0.15, "weight_lc": 0.05, "weight_gh": 0.20,
        "weight_skill_pct": 60, "weight_cgpa_pct": 15, "weight_lc_pct": 5, "weight_gh_pct": 20,
        "avg_salary": "₹5–25 LPA", "demand_trend": "Growing ↑", "demand_level": "growing",
        "salary_level": "medium", "difficulty": "Low–Medium", "time_to_ready": "4–8 months",
        "job_roles": ["UI Designer", "UX Designer", "Product Designer", "Design Lead", "Head of Design"],
        "top_companies": ["Zomato", "Swiggy", "Razorpay", "Urban Company", "Paytm", "BYJU'S", "Adobe"],
        "certifications": ["Google UX Design Certificate", "Figma Professional", "Interaction Design Foundation"],
        "day_in_life": "Create wireframes and prototypes, conduct user research, run usability tests, collaborate with developers via Figma handoff.",
        "growth_path": "Junior Designer → UX Designer → Product Designer → Design Lead → Head of Design",
        "growth_steps": ["Junior Designer", "UX Designer", "Product Designer", "Design Lead", "Head of Design"],
        "radar_labels": ["Figma", "User Research", "Visual Design", "Prototyping", "HTML/CSS", "Collaboration"],
        "radar_required": [9, 8, 9, 8, 6, 8],
        "city_demand": [
            {"city": "Bangalore",  "demand": "🔥 Highest",  "openings": "3,500+", "why": "Product-first startups, SaaS companies, design studios"},
            {"city": "Mumbai",     "demand": "🔥 Very High","openings": "2,800+", "why": "Media, fashion-tech, fintech UX, advertising agencies"},
            {"city": "Delhi NCR",  "demand": "📈 High",      "openings": "2,000+", "why": "EdTech design, D2C brands, government app design"},
            {"city": "Pune",       "demand": "📊 Moderate",  "openings": "1,400+", "why": "IT product design teams, gaming UI, auto UX"},
            {"city": "Hyderabad",  "demand": "📊 Moderate",  "openings": "1,200+", "why": "SaaS product design, Microsoft design centre"},
            {"city": "Remote",     "demand": "🔥 Very High","openings": "4,000+", "why": "Remote design is booming globally — Dribbble, Toptal, Contra"},
        ],
        "roadmap": [
            {"week": "Week 1–2",   "title": "Design Principles",        "desc": "Typography, colour theory, layout, visual hierarchy. Analyse 10 apps.",          "resources": ["Refactoring UI", "Dribbble"]},
            {"week": "Week 3–5",   "title": "Figma Mastery",            "desc": "Components, variants, auto-layout, prototyping, and dev handoff.",               "resources": ["Figma Academy", "DesignCode"]},
            {"week": "Week 6–8",   "title": "User Research & UX",       "desc": "Conduct 5 user interviews. Build journey maps and personas.",                   "resources": ["Nielsen Norman", "IDEO Design Kit"]},
            {"week": "Week 9–10",  "title": "Case Study Projects",      "desc": "Redesign 2 real apps. Document your process with before/after.",                "resources": ["UX Collective", "Medium"]},
            {"week": "Week 11–12", "title": "Portfolio & Job Hunt",     "desc": "Build a Behance/personal site portfolio. Apply to 20+ design roles.",           "resources": ["Behance", "Contra", "Dribbble Jobs"]},
        ],
        "salary": [
            {"city": "Bangalore", "range": "₹5–25 LPA",  "exp": "0–5 yrs"},
            {"city": "Mumbai",    "range": "₹6–28 LPA",  "exp": "0–5 yrs"},
            {"city": "Delhi NCR", "range": "₹5–22 LPA",  "exp": "0–5 yrs"},
            {"city": "Pune",      "range": "₹4–18 LPA",  "exp": "0–5 yrs"},
            {"city": "Hyderabad", "range": "₹4–18 LPA",  "exp": "0–5 yrs"},
            {"city": "Remote",    "range": "₹8–40 LPA",  "exp": "1+ yrs"},
        ],
    },

    # ── 9 ─────────────────────────────────────────
    "Embedded Systems / IoT Engineer": {
        "icon": "⚙️",
        "desc": "Program hardware and build connected devices. Growing with EV and Industry 4.0.",
        "required_skills": ["C++", "Python", "Microcontrollers", "Arduino", "RTOS", "Networking", "Linux"],
        "weight_skill": 0.65, "weight_cgpa": 0.20, "weight_lc": 0.05, "weight_gh": 0.10,
        "weight_skill_pct": 65, "weight_cgpa_pct": 20, "weight_lc_pct": 5, "weight_gh_pct": 10,
        "avg_salary": "₹5–28 LPA", "demand_trend": "Growing ↑", "demand_level": "growing",
        "salary_level": "medium", "difficulty": "Hard", "time_to_ready": "8–14 months",
        "job_roles": ["Embedded Engineer", "Firmware Developer", "IoT Engineer", "VLSI Engineer", "Robotics Engineer"],
        "top_companies": ["Bosch", "Texas Instruments", "Qualcomm", "Intel", "Ola Electric", "ISRO", "Tata Elxsi"],
        "certifications": ["ARM Cortex Certified", "AWS IoT Core", "Coursera Embedded Systems Specialisation"],
        "day_in_life": "Write firmware in C/C++, debug hardware with oscilloscopes, integrate sensors, build device communication protocols.",
        "growth_path": "Embedded Eng → Sr Firmware Dev → Systems Architect → Lead Engineer → VP Engineering",
        "growth_steps": ["Embedded Eng", "Sr Firmware Dev", "Systems Architect", "Lead Engineer", "VP Engineering"],
        "radar_labels": ["C/C++", "Microcontrollers", "RTOS", "Hardware Debugging", "Networking/Protocols", "Linux"],
        "radar_required": [9, 9, 8, 8, 7, 7],
        "city_demand": [
            {"city": "Bangalore",  "demand": "🔥 Highest",  "openings": "4,000+", "why": "Bosch, Qualcomm, Texas Instruments, Ola Electric all based here"},
            {"city": "Pune",       "demand": "🔥 Very High","openings": "3,200+", "why": "Automotive OEM suppliers, Tata, Mahindra EV electronics"},
            {"city": "Hyderabad",  "demand": "📈 High",      "openings": "2,200+", "why": "Defence electronics, BHEL, semiconductor design centres"},
            {"city": "Chennai",    "demand": "📈 High",      "openings": "2,000+", "why": "Automotive embedded (Ford, BMW R&D), Ashok Leyland"},
            {"city": "Delhi NCR",  "demand": "📊 Moderate",  "openings": "1,500+", "why": "DRDO, ISRO centres, smart city IoT projects"},
            {"city": "Ahmedabad",  "demand": "📊 Moderate",  "openings": "800+",   "why": "Industrial IoT, GIDC electronics, solar power electronics"},
        ],
        "roadmap": [
            {"week": "Week 1–2",   "title": "C/C++ for Embedded",       "desc": "Pointers, memory management, bit manipulation. Essential for firmware.",        "resources": ["Neso Academy", "Embedded.fm"]},
            {"week": "Week 3–5",   "title": "Microcontrollers & Arduino","desc": "GPIO, UART, SPI, I2C. Build 5 sensor projects.",                              "resources": ["Arduino Docs", "Circuit Digest"]},
            {"week": "Week 6–8",   "title": "RTOS Basics",              "desc": "FreeRTOS tasks, queues, semaphores. Run on STM32 or ESP32.",                   "resources": ["FreeRTOS Docs", "DigiKey Academy"]},
            {"week": "Week 9–10",  "title": "IoT & Connectivity",       "desc": "MQTT, WiFi, BLE protocols. Connect device to AWS IoT or Firebase.",            "resources": ["AWS IoT Core", "Random Nerd Tutorials"]},
            {"week": "Week 11–12", "title": "Capstone Project",         "desc": "Build a complete IoT product: sensor → MCU → cloud → dashboard.",             "resources": ["Hackster.io", "Instructables"]},
        ],
        "salary": [
            {"city": "Bangalore", "range": "₹5–28 LPA",  "exp": "0–5 yrs"},
            {"city": "Pune",      "range": "₹5–24 LPA",  "exp": "0–5 yrs"},
            {"city": "Hyderabad", "range": "₹5–22 LPA",  "exp": "0–5 yrs"},
            {"city": "Chennai",   "range": "₹5–20 LPA",  "exp": "0–5 yrs"},
            {"city": "Delhi NCR", "range": "₹5–22 LPA",  "exp": "0–5 yrs"},
            {"city": "Remote",    "range": "₹8–35 LPA",  "exp": "3+ yrs"},
        ],
    },

    # ── 10 ────────────────────────────────────────
    "Blockchain / Web3 Developer": {
        "icon": "⛓️",
        "desc": "Build decentralised applications, smart contracts, and DeFi protocols.",
        "required_skills": ["Solidity", "Python", "JavaScript", "Blockchain", "Smart Contracts", "SQL", "Networking"],
        "weight_skill": 0.70, "weight_cgpa": 0.10, "weight_lc": 0.10, "weight_gh": 0.10,
        "weight_skill_pct": 70, "weight_cgpa_pct": 10, "weight_lc_pct": 10, "weight_gh_pct": 10,
        "avg_salary": "₹10–60 LPA", "demand_trend": "Volatile ↕", "demand_level": "growing",
        "salary_level": "very_high", "difficulty": "Hard", "time_to_ready": "8–14 months",
        "job_roles": ["Smart Contract Dev", "Solidity Engineer", "DeFi Developer", "Web3 Full-Stack", "Blockchain Architect"],
        "top_companies": ["Polygon", "CoinDCX", "WazirX", "Coinbase India", "Consensys", "Chainlink", "CoinSwitch"],
        "certifications": ["Ethereum Developer (EatTheBlocks)", "Alchemy University", "ConsenSys Academy"],
        "day_in_life": "Write and audit smart contracts, build dApps with ethers.js, integrate wallets, test on testnets, monitor on-chain activity.",
        "growth_path": "Jr Solidity Dev → Solidity Engineer → Senior Dev → Protocol Engineer → CTO",
        "growth_steps": ["Jr Solidity Dev", "Solidity Engineer", "Senior Dev", "Protocol Engineer", "CTO"],
        "radar_labels": ["Solidity", "JavaScript/Web3", "DeFi Concepts", "Security/Auditing", "Cryptography", "Networking"],
        "radar_required": [9, 8, 8, 8, 7, 6],
        "city_demand": [
            {"city": "Bangalore",  "demand": "🔥 Highest",  "openings": "1,800+", "why": "Polygon, CoinDCX, CoinSwitch HQ — India's Web3 capital"},
            {"city": "Mumbai",     "demand": "🔥 Very High","openings": "1,400+", "why": "WazirX, Nuo Network, BFSI blockchain adoption"},
            {"city": "Delhi NCR",  "demand": "📈 High",      "openings": "900+",   "why": "Government blockchain pilots, startup ecosystem"},
            {"city": "Hyderabad",  "demand": "📊 Moderate",  "openings": "600+",   "why": "Blockchain for supply chain, healthcare records"},
            {"city": "Remote",     "demand": "🔥 Highest",  "openings": "10,000+","why": "Web3 is globally remote-first — most protocols pay in crypto"},
            {"city": "Global",     "demand": "🔥 Very High","openings": "50,000+","why": "USD salaries, DAOs hire globally regardless of location"},
        ],
        "roadmap": [
            {"week": "Week 1–2",   "title": "Blockchain Fundamentals",  "desc": "How Bitcoin/Ethereum work, consensus mechanisms, wallets and keys.",             "resources": ["Mastering Ethereum", "Blockchain at Berkeley"]},
            {"week": "Week 3–5",   "title": "Solidity & Smart Contracts","desc": "Write ERC-20, ERC-721 tokens. Deploy on Sepolia testnet with Hardhat.",        "resources": ["Solidity Docs", "CryptoZombies"]},
            {"week": "Week 6–8",   "title": "Web3.js / Ethers.js",      "desc": "Connect frontend to blockchain. Build a simple dApp with MetaMask.",            "resources": ["ethers.js Docs", "EatTheBlocks"]},
            {"week": "Week 9–10",  "title": "DeFi & Security",          "desc": "Understand AMMs, liquidity pools. Audit contracts with Slither.",               "resources": ["Uniswap Docs", "Trail of Bits"]},
            {"week": "Week 11–12", "title": "Deploy dApp & Get Grants", "desc": "Deploy on mainnet. Apply to Gitcoin, Alchemy, or Polygon grants.",             "resources": ["Gitcoin", "Alchemy University", "Polygon ID"]},
        ],
        "salary": [
            {"city": "Bangalore", "range": "₹10–60 LPA", "exp": "0–5 yrs"},
            {"city": "Mumbai",    "range": "₹10–55 LPA", "exp": "0–5 yrs"},
            {"city": "Remote IN", "range": "₹15–80 LPA", "exp": "1+ yrs"},
            {"city": "Remote US", "range": "$80–200K",   "exp": "1+ yrs"},
            {"city": "DAO/DeFi",  "range": "$60–300K",   "exp": "Any"},
            {"city": "Global",    "range": "Crypto + equity", "exp": "Any"},
        ],
    },

}


def normalize(value: float, max_value: float) -> float:
    return min(value / max_value, 1.0) if max_value > 0 else 0.0


def score_career(career_name: str, profile: dict, student: dict) -> float:
    required      = set(profile["required_skills"])
    user_sk       = set(student.get("skills", []))
    skill_overlap = len(required & user_sk) / len(required) if required else 0
    cgpa_norm     = normalize(student.get("cgpa",     0), 10)
    lc_norm       = normalize(student.get("leetcode", 0), 300)
    gh_norm       = normalize(student.get("github",   0), 15)
    raw = (
        profile["weight_skill"] * skill_overlap +
        profile["weight_cgpa"]  * cgpa_norm     +
        profile["weight_lc"]    * lc_norm       +
        profile["weight_gh"]    * gh_norm
    )
    return min(round(18 + raw * 80), 98)


def score_breakdown(profile: dict, student: dict) -> dict:
    required      = set(profile["required_skills"])
    user_sk       = set(student.get("skills", []))
    skill_overlap = len(required & user_sk) / len(required) if required else 0
    cgpa_norm     = normalize(student.get("cgpa",     0), 10)
    lc_norm       = normalize(student.get("leetcode", 0), 300)
    gh_norm       = normalize(student.get("github",   0), 15)

    base      = 18
    skill_pts = round(profile["weight_skill"] * skill_overlap * 80)
    cgpa_pts  = round(profile["weight_cgpa"]  * cgpa_norm    * 80)
    lc_pts    = round(profile["weight_lc"]    * lc_norm      * 80)
    gh_pts    = round(profile["weight_gh"]    * gh_norm      * 80)

    skill_pct = round(len(required & user_sk) / len(required) * 100) if required else 0
    cgpa_pct  = round(cgpa_norm * 100)
    lc_pct    = round(lc_norm   * 100)
    gh_pct    = round(gh_norm   * 100)

    return {
        "skill_pts": skill_pts, "cgpa_pts": cgpa_pts,
        "lc_pts":    lc_pts,    "gh_pts":   gh_pts,
        "base_pts":  base,
        "skill_pct": skill_pct, "cgpa_pct": cgpa_pct,
        "lc_pct":    lc_pct,    "gh_pct":   gh_pct,
        "skill_weight": profile["weight_skill_pct"],
        "cgpa_weight":  profile["weight_cgpa_pct"],
        "lc_weight":    profile["weight_lc_pct"],
        "gh_weight":    profile["weight_gh_pct"],
    }


def recommend(student: dict) -> list:
    results = []
    for name, profile in CAREER_PROFILES.items():
        sc        = score_career(name, profile, student)
        breakdown = score_breakdown(profile, student)
        have      = [s for s in student.get("skills", []) if s in profile["required_skills"]]
        missing   = [s for s in profile["required_skills"] if s not in student.get("skills", [])]
        results.append({
            "career":         name,
            "icon":           profile["icon"],
            "desc":           profile["desc"],
            "score":          sc,
            "breakdown":      breakdown,
            "skills_have":    have,
            "skills_missing": missing,
            "avg_salary":     profile["avg_salary"],
            "demand_trend":   profile["demand_trend"],
            "roadmap":        profile["roadmap"],
            "salary":         profile["salary"],
            "city_demand":    profile.get("city_demand", []),
            "radar_labels":   profile["radar_labels"],
            "radar_required": profile["radar_required"],
        })
    return sorted(results, key=lambda x: x["score"], reverse=True)
