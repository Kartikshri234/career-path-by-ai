"""
resume_screener/screener_service.py
All heavy logic: text extraction, scoring, ATS, company matching, interview tracks.
Kept separate from views.py so views stay thin and readable.
"""
import os
import re
from collections import Counter
from typing import Any, cast

import fitz          # PyMuPDF
import docx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from werkzeug.utils import secure_filename

from django.conf import settings

# ── Upload folder ──────────────────────────────────────────────────────────────
UPLOAD_DIR = os.path.join(settings.BASE_DIR, 'resume_screener', 'uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ── Action verbs ───────────────────────────────────────────────────────────────
ACTION_VERBS = [
    "achieved", "architected", "automated", "built", "collaborated",
    "created", "decreased", "delivered", "deployed", "designed", "developed",
    "drove", "engineered", "enhanced", "improved", "implemented",
    "increased", "launched", "led", "managed", "mentored", "optimized",
    "reduced", "refactored", "scaled", "shipped", "streamlined", "integrated",
]

# ── Skill keywords ─────────────────────────────────────────────────────────────
SKILL_KEYWORDS = [
    "python", "java", "javascript", "typescript", "c++", "c#", "golang", "rust",
    "swift", "kotlin", "php", "ruby", "scala", "r",
    "react", "vue", "angular", "next.js", "node.js", "django", "flask", "fastapi",
    "spring", "html", "css", "tailwind", "bootstrap",
    "machine learning", "deep learning", "tensorflow", "pytorch", "keras",
    "scikit-learn", "pandas", "numpy", "data analysis", "nlp", "computer vision",
    "sql", "mysql", "postgresql", "mongodb", "redis", "elasticsearch",
    "aws", "azure", "gcp", "docker", "kubernetes", "ci/cd", "jenkins",
    "github actions", "terraform", "ansible", "linux", "git",
    "rest api", "graphql", "microservices", "agile", "scrum",
    "figma", "excel", "power bi", "tableau",
    "leadership", "communication", "teamwork", "problem solving",
]

STOP_WORDS = {
    "and", "the", "for", "with", "from", "that", "this", "are", "was", "were",
    "has", "have", "been", "will", "would", "could", "should", "our", "your",
    "their", "we", "you", "they", "all", "any", "not", "can", "may", "also",
    "more", "other", "some", "such", "each", "both", "its", "into", "about",
    "over", "under", "then", "than", "when", "where", "which", "while",
    "through", "these", "those", "being", "having", "using", "making",
    "including", "working", "responsible", "required", "preferred",
    "experience", "years", "year", "strong", "excellent", "ability",
    "skills", "knowledge", "understanding", "familiarity", "proficiency",
}

# ── Company database ───────────────────────────────────────────────────────────
COMPANY_DATABASE = [
    {"name": "Google",  "logo": "🔵", "domain": ["software","ai","machine learning","data","cloud","python","golang","c++","algorithms"],    "interview_focus": ["Data Structures & Algorithms","System Design","Behavioural"], "rounds": 5, "difficulty": "Very High", "type": "Product",   "size": "100k+",  "tips": "Focus heavily on DSA and system design. Google values scalable thinking."},
    {"name": "Microsoft","logo": "🟦","domain": ["software","azure","cloud","c#","java","typescript","devops","sql"],                          "interview_focus": ["Coding","System Design","Behavioural"],                       "rounds": 4, "difficulty": "High",      "type": "Product",   "size": "100k+",  "tips": "Emphasize collaboration and growth mindset. Strong on cloud and enterprise."},
    {"name": "Amazon",  "logo": "🟧", "domain": ["software","aws","cloud","java","python","devops","leadership","e-commerce","data"],          "interview_focus": ["Leadership Principles","Coding","System Design"],            "rounds": 5, "difficulty": "Very High", "type": "Product",   "size": "100k+",  "tips": "Memorize all 16 Leadership Principles. STAR format for behavioural."},
    {"name": "Meta",    "logo": "🔷", "domain": ["software","react","python","c++","machine learning","social","mobile","ios","android"],      "interview_focus": ["Coding","System Design","Behavioural"],                       "rounds": 5, "difficulty": "Very High", "type": "Product",   "size": "50k+",   "tips": "Speed and accuracy in coding is paramount. React experience is a plus."},
    {"name": "Infosys", "logo": "🟩", "domain": ["java","sql","software","consulting","testing","bpo","support","manual testing"],             "interview_focus": ["Technical MCQ","Coding Round","HR Interview"],               "rounds": 3, "difficulty": "Medium",    "type": "Service",   "size": "300k+",  "tips": "Strong on communication and aptitude. Java and SQL basics are key."},
    {"name": "TCS",     "logo": "🟪", "domain": ["java","sql","testing","support","consulting","software","bpo","data entry"],                 "interview_focus": ["Aptitude","Technical Interview","HR Round"],                 "rounds": 3, "difficulty": "Medium",    "type": "Service",   "size": "600k+",  "tips": "Focus on aptitude, reasoning, and verbal ability for NQT exam."},
    {"name": "Wipro",   "logo": "🔶", "domain": ["java","sql","testing","support","consulting","software","cloud","devops"],                   "interview_focus": ["NLTH Exam","Technical Interview","HR Round"],               "rounds": 3, "difficulty": "Medium",    "type": "Service",   "size": "250k+",  "tips": "NLTH covers aptitude and coding."},
    {"name": "Accenture","logo":"🟣", "domain": ["consulting","java","testing","cloud","management","data","agile","business analysis"],       "interview_focus": ["Cognitive Test","Technical Interview","HR"],                 "rounds": 3, "difficulty": "Medium",    "type": "Service",   "size": "700k+",  "tips": "Communication skills are critical. Strong on consulting and BPO."},
    {"name": "Flipkart","logo": "🟡", "domain": ["software","java","python","react","data","machine learning","e-commerce","sql","system design"],"interview_focus": ["Coding","System Design","Behavioural"],                  "rounds": 4, "difficulty": "High",      "type": "Product",   "size": "30k+",   "tips": "Strong DSA and system design for backend/SDE roles."},
    {"name": "Zoho",    "logo": "🔴", "domain": ["java","c","c++","software","saas","sql","problem solving","algorithms"],                     "interview_focus": ["Aptitude","Technical Coding","Technical Interview","HR"],    "rounds": 4, "difficulty": "High",      "type": "Product",   "size": "12k+",   "tips": "Zoho values self-taught engineers. Aptitude and C/Java coding focus."},
    {"name": "Startups","logo": "🚀", "domain": ["react","node.js","python","flask","django","mobile","startup","agile","devops","fullstack"], "interview_focus": ["Portfolio/Projects","Practical Coding","Culture Fit"],      "rounds": 2, "difficulty": "Medium",    "type": "Startup",   "size": "<500",   "tips": "Show side projects, GitHub activity, and ability to wear multiple hats."},
    {"name": "Data Science Firms","logo":"📊","domain": ["machine learning","deep learning","python","tensorflow","pytorch","data analysis","sql","statistics","nlp","tableau","power bi"], "interview_focus": ["Statistics/ML Concepts","Python Coding","Case Study"], "rounds": 3, "difficulty": "High", "type": "Analytics", "size": "Varies", "tips": "Strong foundation in statistics, probability, and ML algorithms required."},
]

# ── Interview stage tracks ─────────────────────────────────────────────────────
INTERVIEW_STAGES = {
    "freshers": {
        "label": "Fresher Track",
        "stages": [
            {"name": "Aptitude & Reasoning",  "icon": "🧮", "desc": "Quantitative, logical reasoning, verbal. 30–60 min online test.", "prep": "Practice 20 mock tests. Focus on speed and accuracy."},
            {"name": "Technical Written",      "icon": "💻", "desc": "MCQs on CS fundamentals, DBMS, OS, Networks.", "prep": "Revise CS fundamentals, data structures, and basic SQL."},
            {"name": "Coding Round",           "icon": "⌨️", "desc": "2–3 coding problems on arrays, strings, patterns. Easy–medium.", "prep": "Solve 50 problems on LeetCode/HackerRank before appearing."},
            {"name": "Technical Interview",    "icon": "🔬", "desc": "Deep dive on projects, internships, core CS subjects.", "prep": "Prepare STAR stories for every project. Know your resume cold."},
            {"name": "HR Round",               "icon": "🤝", "desc": "Introduction, salary, situation-based questions.", "prep": "Research the company, know your strengths/weaknesses."},
        ],
    },
    "junior": {
        "label": "Junior Developer (1–3 yrs)",
        "stages": [
            {"name": "Online Coding Assessment","icon": "⌨️", "desc": "2–4 medium problems. Time-boxed at 90 mins.", "prep": "Practice medium LeetCode. Focus on arrays, trees, DP basics."},
            {"name": "Technical Phone Screen", "icon": "📞", "desc": "30 min call: code in shared editor + CS concepts.", "prep": "Practice live coding on CoderPad. Explain thought process clearly."},
            {"name": "Technical Interview ×2", "icon": "💡", "desc": "One DSA-focused, one on your tech stack.", "prep": "Review system design basics and your framework deeply."},
            {"name": "Behavioural Round",      "icon": "🎭", "desc": "STAR-format questions on teamwork, conflict, leadership.", "prep": "Prepare 6–8 STAR stories covering different competencies."},
            {"name": "Manager Round",          "icon": "🏢", "desc": "Culture fit, long-term goals, team match discussion.", "prep": "Know why you want THIS company. Have 3 good questions ready."},
        ],
    },
    "mid": {
        "label": "Mid-Level Engineer (3–6 yrs)",
        "stages": [
            {"name": "Coding Assessment",      "icon": "⌨️", "desc": "Medium–hard problems. 2–3 questions in 2 hours.", "prep": "Focus on medium-hard LeetCode, DP, graphs, system-level thinking."},
            {"name": "System Design",          "icon": "🏗️", "desc": "Design a scalable system: URL shortener, Twitter feed, Uber, etc.", "prep": "Study 'Designing Data-Intensive Applications'. Practice 10 designs."},
            {"name": "Technical Deep Dive",    "icon": "🔭", "desc": "Architecture of past projects, trade-offs, debugging.", "prep": "Be ready to whiteboard your last 3 major projects."},
            {"name": "Behavioural / Leadership","icon":"🎯", "desc": "Own team impact, mentoring, cross-team collaboration.", "prep": "Show ownership. Companies want builders, not just coders."},
            {"name": "Hiring Manager Round",   "icon": "📋", "desc": "Final round checking culture, ambition, long-term fit.", "prep": "Know the company's product deeply. Have 5 smart questions."},
        ],
    },
    "senior": {
        "label": "Senior / Lead Engineer (6+ yrs)",
        "stages": [
            {"name": "System Design (×2)",     "icon": "🏗️", "desc": "Large-scale distributed systems. Consensus, sharding, CAP theorem.", "prep": "Practice 20+ system design problems. Read 'DDIA' book fully."},
            {"name": "Advanced Coding",        "icon": "⌨️", "desc": "Hard LeetCode. Focus on optimisation, complexity analysis.", "prep": "Solve 100+ hard problems. Explain trade-offs clearly."},
            {"name": "Leadership & Execution", "icon": "🚀", "desc": "How you drove projects, made decisions, unblocked teams.", "prep": "Have 10+ impactful leadership stories. Quantify everything."},
            {"name": "Cross-functional",       "icon": "🌐", "desc": "Working with product, design, data teams.", "prep": "Show breadth: you've influenced roadmaps, not just written code."},
            {"name": "VP / Director Round",    "icon": "🏛️", "desc": "Strategic thinking, vision alignment, company growth mindset.", "prep": "Research company strategy and OKRs. Align your vision with theirs."},
        ],
    },
}


# ── Text extraction ────────────────────────────────────────────────────────────

def extract_text_from_pdf(file_path: str) -> str:
    parts = []
    pdf = fitz.open(file_path)
    for page in pdf:
        t = page.get_text("text")
        parts.append(t if isinstance(t, str) else "")
    return " ".join(parts)


def extract_text_from_docx(file_path: str) -> str:
    doc = docx.Document(file_path)
    return " ".join(p.text for p in doc.paragraphs)


def read_resume(file_path: str) -> str:
    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    if file_path.endswith(".docx"):
        return extract_text_from_docx(file_path)
    return ""


# ── Scoring helpers ────────────────────────────────────────────────────────────

def get_similarity(job_desc: str, resume_text: str) -> float:
    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform([job_desc, resume_text])
    dense = cast(Any, vectors).toarray()
    score = cosine_similarity(dense[0:1], dense[1:2])
    return round(float(score[0][0]) * 100, 2)


def extract_skills(text: str) -> list:
    text_lower = text.lower()
    found = []
    for skill in SKILL_KEYWORDS:
        if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
            found.append(skill.title() if len(skill) <= 3 else skill.capitalize())
    return list(dict.fromkeys(found))


def extract_top_keywords(text: str, top_n: int = 15) -> list:
    words = re.findall(r'\b[a-zA-Z][a-zA-Z+#.]{2,}\b', text.lower())
    filtered = [w for w in words if w not in STOP_WORDS and len(w) > 3]
    counter = Counter(filtered)
    return [word for word, _ in counter.most_common(top_n)]


def keyword_overlap(jd_keywords: list, resume_text: str):
    text_lower = resume_text.lower()
    matched = [kw for kw in jd_keywords if re.search(r'\b' + re.escape(kw) + r'\b', text_lower)]
    missing = [kw for kw in jd_keywords if kw not in matched]
    return matched, missing


def word_count(text: str) -> int:
    return len(text.split())


def extract_experience_years(text: str) -> int:
    patterns = [
        r'(\d+)\+?\s*years?\s*(?:of\s*)?(?:experience|exp)',
        r'(\d+)\+?\s*yrs?\s*(?:of\s*)?(?:experience|exp)',
        r'experience\s*(?:of\s*)?(\d+)\+?\s*years?',
    ]
    found = []
    for p in patterns:
        for m in re.finditer(p, text.lower()):
            try:
                found.append(int(m.group(1)))
            except (IndexError, ValueError):
                pass
    return max(found) if found else 0


def count_action_verbs(text: str):
    text_lower = text.lower()
    found = [v for v in ACTION_VERBS if re.search(r'\b' + v + r'\b', text_lower)]
    return len(found), found


def has_quantified_achievements(text: str) -> bool:
    pattern = r'(?:reduced|improved|increased|decreased|saved|grew|achieved|delivered|boosted)[^.\n]{0,60}\d+[%x]'
    return bool(re.search(pattern, text.lower()))


def detect_education(text: str) -> str:
    text_lower = text.lower()
    if any(k in text_lower for k in ['phd', 'ph.d', 'doctorate']):
        return 'PhD'
    if any(k in text_lower for k in ['m.tech', 'mtech', 'm.e.', 'mba', 'master']):
        return 'Masters'
    if any(k in text_lower for k in ['b.tech', 'btech', 'b.e.', 'b.sc', 'bachelor', 'undergraduate']):
        return 'Bachelors'
    if any(k in text_lower for k in ['diploma', 'polytechnic']):
        return 'Diploma'
    return 'Unknown'


def get_strength(score: float) -> dict:
    if score >= 75:
        return {"label": "Excellent Match", "color": "emerald", "emoji": "🏆", "tier": "A"}
    if score >= 55:
        return {"label": "Strong Match", "color": "cyan", "emoji": "✅", "tier": "B"}
    if score >= 35:
        return {"label": "Moderate Match", "color": "amber", "emoji": "🟡", "tier": "C"}
    return {"label": "Weak Match", "color": "rose", "emoji": "🔴", "tier": "D"}


def compute_ats_score(resume_text: str):
    text_lower = resume_text.lower()
    checks = {}
    total = 0
    possible = 0

    # Sections
    sections = {
        "experience": ["experience", "work experience", "employment", "professional experience"],
        "education":  ["education", "academic", "qualification", "degree"],
        "skills":     ["skills", "technical skills", "core competencies", "technologies"],
        "summary":    ["summary", "objective", "profile", "about me", "overview"],
    }
    found_sections = [sec for sec, kws in sections.items() if any(k in text_lower for k in kws)]
    total += len(found_sections) * 6
    possible += 24
    checks["sections"] = {"found": found_sections, "missing": [s for s in sections if s not in found_sections], "score": len(found_sections) * 6, "max": 24}

    # Contact
    has_email = bool(re.search(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', resume_text))
    has_phone = bool(re.search(r'(\+?\d[\d\s\-\(\)]{7,14}\d)', resume_text))
    has_linkedin = "linkedin" in text_lower
    contact_score = (8 if has_email else 0) + (7 if has_phone else 0) + (5 if has_linkedin else 0)
    total += contact_score
    possible += 20
    checks["contact"] = {"email": has_email, "phone": has_phone, "linkedin": has_linkedin, "score": contact_score, "max": 20}

    # Dates
    date_patterns = [r'\b(19|20)\d{2}\b', r'\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s+(19|20)\d{2}\b', r'\b(0?[1-9]|1[0-2])\s*/\s*(19|20)\d{2}\b']
    has_dates = any(re.search(p, text_lower) for p in date_patterns)
    total += 20 if has_dates else 0
    possible += 20
    checks["dates"] = {"found": has_dates, "score": 20 if has_dates else 0, "max": 20}

    # Length
    wc = word_count(resume_text)
    if 300 <= wc <= 700:
        len_score, len_note = 20, "Ideal length"
    elif 200 <= wc < 300 or 700 < wc <= 900:
        len_score, len_note = 12, "Slightly short" if wc < 300 else "Slightly long"
    elif wc < 200:
        len_score, len_note = 4, "Too short"
    else:
        len_score, len_note = 6, "Too long"
    total += len_score
    possible += 20
    checks["length"] = {"word_count": wc, "score": len_score, "max": 20, "note": len_note}

    # Formatting
    words = resume_text.split()
    avg_word_len = sum(len(w) for w in words) / max(len(words), 1)
    good_format = avg_word_len < 14
    total += 16 if good_format else 0
    possible += 16
    checks["formatting"] = {"parseable": good_format, "score": 16 if good_format else 0, "max": 16, "note": "Text parsed cleanly" if good_format else "Possible table/column layout — may confuse ATS"}

    ats_score = round((total / possible) * 100) if possible > 0 else 0
    return ats_score, checks


def generate_improvement_tips(result_data: dict, jd_text: str) -> list:
    tips = []
    score          = result_data.get('score', 0)
    ats            = result_data.get('ats_score', 0)
    wc             = result_data.get('word_count', 0)
    action_count   = result_data.get('action_verb_count', 0)
    has_quant      = result_data.get('has_quantified', False)
    missing_skills = result_data.get('missing_skills', [])
    missing_kw     = result_data.get('missing_keywords', [])
    ats_details    = result_data.get('ats_details', {})

    if missing_skills:
        tips.append({'icon': '🎯', 'text': f'Add missing skills: <strong>{", ".join(missing_skills[:3])}</strong> — these appear in the job description.'})
    if not has_quant:
        tips.append({'icon': '📊', 'text': 'Add <strong>quantified achievements</strong> — e.g. "Reduced API latency by 35%".'})
    if action_count < 5:
        tips.append({'icon': '✍️', 'text': 'Use stronger <strong>action verbs</strong> (e.g. Architected, Optimized, Delivered, Shipped).'})
    if wc < 300:
        tips.append({'icon': '📝', 'text': f'Resume is too short ({wc} words). Add more detail to experience bullets.'})
    elif wc > 900:
        tips.append({'icon': '✂️', 'text': f'Resume is too long ({wc} words). Trim to 400–700 words for optimal ATS readability.'})
    if not ats_details.get('contact', {}).get('linkedin'):
        tips.append({'icon': '🔗', 'text': 'Add a <strong>LinkedIn profile URL</strong> — most ATS systems expect it.'})
    if not ats_details.get('contact', {}).get('email'):
        tips.append({'icon': '📧', 'text': 'No email detected — ensure contact info is plain text, not inside an image.'})
    missing_sections = ats_details.get('sections', {}).get('missing', [])
    if 'summary' in missing_sections:
        tips.append({'icon': '💡', 'text': 'Add a <strong>Professional Summary</strong> — 2–3 lines tailored to this role.'})
    if missing_kw:
        tips.append({'icon': '🔑', 'text': f'Include keywords from JD: <strong>{", ".join(missing_kw[:4])}</strong>.'})
    if score < 40:
        tips.append({'icon': '🔄', 'text': 'Tailor this resume specifically for this role — a generic resume scores much lower.'})
    if ats < 50:
        tips.append({'icon': '🤖', 'text': 'Low ATS score — avoid columns, graphics, or tables. Use a clean single-column layout.'})
    return tips[:6]


# ── Interview track & company match ───────────────────────────────────────────

def get_interview_track(exp_years: int) -> dict:
    if exp_years == 0:
        return INTERVIEW_STAGES["freshers"]
    if exp_years <= 3:
        return INTERVIEW_STAGES["junior"]
    if exp_years <= 6:
        return INTERVIEW_STAGES["mid"]
    return INTERVIEW_STAGES["senior"]


def match_companies(skills: list, exp_years: int, target_role: str = "", preferred_type: str = "") -> list:
    skill_lower = [s.lower() for s in skills]
    jd_lower = target_role.lower()
    scored = []
    for company in COMPANY_DATABASE:
        match_score = 0
        for kw in company["domain"]:
            if any(kw in s for s in skill_lower):
                match_score += 10
            if kw in jd_lower:
                match_score += 5
        if exp_years == 0 and company["type"] == "Service":
            match_score += 15
        elif exp_years >= 4 and company["type"] == "Product":
            match_score += 10
        elif exp_years >= 2 and company["type"] == "Startup":
            match_score += 8
        if preferred_type and preferred_type.lower() in company["type"].lower():
            match_score += 20
        if match_score > 0:
            scored.append({**company, "match_score": match_score})
    scored.sort(key=lambda x: x["match_score"], reverse=True)
    return scored[:5]


# ── Main processing function ───────────────────────────────────────────────────

def process_resume(file, job_desc: str, jd_keywords: list, jd_skills: list) -> dict | None:
    """Save and analyse one uploaded resume file. Returns result dict or None."""
    original_name = file.name or ""
    safe_name = secure_filename(original_name)
    if not safe_name:
        return None

    file_path = os.path.join(UPLOAD_DIR, safe_name)
    with open(file_path, 'wb+') as dest:
        for chunk in file.chunks():
            dest.write(chunk)

    resume_text = read_resume(file_path)
    score = get_similarity(job_desc, resume_text) if job_desc else 0

    resume_skills    = extract_skills(resume_text)
    matched_kw, missing_kw = keyword_overlap(jd_keywords, resume_text)
    matched_skills   = [s for s in jd_skills if s.lower() in resume_text.lower()]
    missing_skills   = [s for s in jd_skills if s.lower() not in resume_text.lower()]

    kw_score    = round(len(matched_kw) / max(len(jd_keywords), 1) * 100)
    skill_score = round(len(matched_skills) / max(len(jd_skills), 1) * 100) if jd_skills else score

    ats_score, ats_details = compute_ats_score(resume_text)
    exp_years = extract_experience_years(resume_text)
    action_count, action_verbs_found = count_action_verbs(resume_text)
    has_quant  = has_quantified_achievements(resume_text)
    education  = detect_education(resume_text)
    strength   = get_strength(score)
    wc         = word_count(resume_text)

    entry = {
        "name": safe_name,
        "score": score,
        "strength": strength,
        "resume_skills": resume_skills[:18],
        "matched_keywords": matched_kw,
        "missing_keywords": missing_kw[:8],
        "matched_skills": matched_skills,
        "missing_skills": missing_skills[:8],
        "kw_score": kw_score,
        "skill_score": skill_score,
        "word_count": wc,
        "ats_score": ats_score,
        "ats_details": ats_details,
        "experience_years": exp_years,
        "action_verb_count": action_count,
        "action_verbs_found": action_verbs_found[:8],
        "has_quantified": has_quant,
        "education": education,
    }
    entry["improvement_tips"] = generate_improvement_tips(entry, job_desc)
    return entry
