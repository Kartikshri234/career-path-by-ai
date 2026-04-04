import os
import re
import json
import uuid
from typing import Any, cast
from collections import Counter

import fitz  # PyMuPDF
import docx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from werkzeug.utils import secure_filename

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.views.decorators.http import require_http_methods

from .models import ScreeningSession, ResumeResult


# ── Upload folder ──
UPLOAD_DIR = os.path.join(settings.BASE_DIR, 'resume_screener', 'uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ── Action verbs ──
ACTION_VERBS = [
    "achieved","architected","automated","built","collaborated","contributed",
    "created","decreased","delivered","deployed","designed","developed",
    "drove","engineered","enhanced","executed","improved","implemented",
    "increased","launched","led","managed","mentored","migrated","optimized",
    "reduced","refactored","released","scaled","shipped","solved","streamlined",
    "transformed","integrated","published","maintained","monitored",
]

# ── Skill keywords ──
SKILL_KEYWORDS = [
    "python","java","javascript","typescript","c++","c#","golang","rust","swift","kotlin","php","ruby","scala","r",
    "react","vue","angular","next.js","node.js","django","flask","fastapi","spring","html","css","tailwind","bootstrap",
    "machine learning","deep learning","tensorflow","pytorch","keras","scikit-learn","pandas","numpy","matplotlib",
    "data analysis","nlp","computer vision","sql","mysql","postgresql","mongodb","redis","elasticsearch",
    "aws","azure","gcp","docker","kubernetes","ci/cd","jenkins","github actions","terraform","ansible","linux",
    "git","rest api","graphql","microservices","agile","scrum","jira","figma","excel","power bi","tableau",
    "leadership","communication","teamwork","problem solving","project management",
]

STOP_WORDS = {
    "and","the","for","with","from","that","this","are","was","were","has","have","been","will","would",
    "could","should","our","your","their","we","you","they","all","any","not","can","may","also","more",
    "other","some","such","each","both","its","into","about","over","under","then","than","when","where",
    "which","while","through","these","those","being","having","using","making","including","working",
    "responsible","required","preferred","experience","years","year","strong","excellent","ability","skills",
    "knowledge","understanding","familiarity","proficiency",
}

# ── Company database for matching ──
COMPANY_DATABASE = [
    {
        "name": "Google",
        "logo": "🔵",
        "domain": ["software","ai","machine learning","data","cloud","python","golang","c++","algorithms"],
        "interview_focus": ["Data Structures & Algorithms", "System Design", "Behavioural"],
        "rounds": 5,
        "difficulty": "Very High",
        "type": "Product",
        "size": "100k+",
        "tips": "Focus heavily on DSA and system design. Google values scalable thinking.",
    },
    {
        "name": "Microsoft",
        "logo": "🟦",
        "domain": ["software","azure","cloud","c#","java","typescript","devops","sql"],
        "interview_focus": ["Coding", "System Design", "Behavioural"],
        "rounds": 4,
        "difficulty": "High",
        "type": "Product",
        "size": "100k+",
        "tips": "Emphasize collaboration and growth mindset. Strong on cloud and enterprise.",
    },
    {
        "name": "Amazon",
        "logo": "🟧",
        "domain": ["software","aws","cloud","java","python","devops","leadership","e-commerce","data"],
        "interview_focus": ["Leadership Principles", "Coding", "System Design"],
        "rounds": 5,
        "difficulty": "Very High",
        "type": "Product",
        "size": "100k+",
        "tips": "Memorize all 16 Leadership Principles. STAR format for behavioural.",
    },
    {
        "name": "Meta",
        "logo": "🔷",
        "domain": ["software","react","python","c++","machine learning","social","mobile","ios","android"],
        "interview_focus": ["Coding", "System Design", "Behavioural"],
        "rounds": 5,
        "difficulty": "Very High",
        "type": "Product",
        "size": "50k+",
        "tips": "Speed and accuracy in coding is paramount. React experience is a plus.",
    },
    {
        "name": "Infosys",
        "logo": "🟩",
        "domain": ["java","sql","software","consulting","testing","bpo","support","manual testing"],
        "interview_focus": ["Technical MCQ", "Coding Round", "HR Interview"],
        "rounds": 3,
        "difficulty": "Medium",
        "type": "Service",
        "size": "300k+",
        "tips": "Strong on communication and aptitude. Java and SQL basics are key.",
    },
    {
        "name": "TCS",
        "logo": "🟪",
        "domain": ["java","sql","testing","support","consulting","software","bpo","data entry"],
        "interview_focus": ["Aptitude", "Technical Interview", "HR Round"],
        "rounds": 3,
        "difficulty": "Medium",
        "type": "Service",
        "size": "600k+",
        "tips": "Focus on aptitude, reasoning, and verbal ability for NQT exam.",
    },
    {
        "name": "Wipro",
        "logo": "🔶",
        "domain": ["java","sql","testing","support","consulting","software","cloud","devops"],
        "interview_focus": ["NLTH Exam", "Technical Interview", "HR Round"],
        "rounds": 3,
        "difficulty": "Medium",
        "type": "Service",
        "size": "250k+",
        "tips": "NLTH (National Level Talent Hunt) covers aptitude and coding.",
    },
    {
        "name": "Accenture",
        "logo": "🟣",
        "domain": ["consulting","java","testing","cloud","management","data","agile","business analysis"],
        "interview_focus": ["Cognitive Test", "Technical Interview", "HR"],
        "rounds": 3,
        "difficulty": "Medium",
        "type": "Service",
        "size": "700k+",
        "tips": "Communication skills are critical. Strong on consulting and BPO.",
    },
    {
        "name": "Flipkart",
        "logo": "🟡",
        "domain": ["software","java","python","react","data","machine learning","e-commerce","sql","system design"],
        "interview_focus": ["Coding", "System Design", "Behavioural"],
        "rounds": 4,
        "difficulty": "High",
        "type": "Product",
        "size": "30k+",
        "tips": "Strong DSA and system design for backend/SDE roles.",
    },
    {
        "name": "Zoho",
        "logo": "🔴",
        "domain": ["java","c","c++","software","saas","sql","problem solving","algorithms"],
        "interview_focus": ["Aptitude", "Technical Coding", "Technical Interview", "HR"],
        "rounds": 4,
        "difficulty": "High",
        "type": "Product",
        "size": "12k+",
        "tips": "Zoho values self-taught engineers. Aptitude and C/Java coding focus.",
    },
    {
        "name": "Startups",
        "logo": "🚀",
        "domain": ["react","node.js","python","flask","django","mobile","startup","agile","devops","fullstack"],
        "interview_focus": ["Portfolio/Projects", "Practical Coding", "Culture Fit"],
        "rounds": 2,
        "difficulty": "Medium",
        "type": "Startup",
        "size": "<500",
        "tips": "Show side projects, GitHub activity, and ability to wear multiple hats.",
    },
    {
        "name": "Data Science Firms",
        "logo": "📊",
        "domain": ["machine learning","deep learning","python","tensorflow","pytorch","data analysis","sql","statistics","nlp","tableau","power bi"],
        "interview_focus": ["Statistics/ML Concepts", "Python Coding", "Case Study"],
        "rounds": 3,
        "difficulty": "High",
        "type": "Analytics",
        "size": "Varies",
        "tips": "Strong foundation in statistics, probability, and ML algorithms required.",
    },
]

# ── Interview section announcer ──
INTERVIEW_STAGES = {
    "freshers": {
        "label": "Fresher Track",
        "stages": [
            {"name": "Aptitude & Reasoning", "icon": "🧮", "desc": "Quantitative, logical reasoning, verbal ability. 30–60 mins online test.", "prep": "Practice 20 mock tests. Focus on speed and accuracy."},
            {"name": "Technical Written", "icon": "💻", "desc": "MCQs on your core subject: CS fundamentals, DBMS, OS, Networks.", "prep": "Revise CS fundamentals, data structures, and basic SQL."},
            {"name": "Coding Round", "icon": "⌨️", "desc": "2–3 coding problems on arrays, strings, patterns. Easy to medium difficulty.", "prep": "Solve 50 problems on LeetCode/HackerRank before appearing."},
            {"name": "Technical Interview", "icon": "🔬", "desc": "Deep dive on your projects, internships, and core CS subjects.", "prep": "Prepare STAR stories for every project. Know your resume cold."},
            {"name": "HR Round", "icon": "🤝", "desc": "Introduction, salary discussion, situation-based questions.", "prep": "Research the company, know your strengths/weaknesses, salary range."},
        ]
    },
    "junior": {
        "label": "Junior Developer (1–3 yrs)",
        "stages": [
            {"name": "Online Coding Assessment", "icon": "⌨️", "desc": "2–4 problems, medium difficulty. Time-boxed at 90 mins.", "prep": "Practice medium LeetCode. Focus on arrays, trees, DP basics."},
            {"name": "Technical Phone Screen", "icon": "📞", "desc": "30 min call: code in shared editor + CS concepts.", "prep": "Practice live coding on CoderPad. Explain your thought process clearly."},
            {"name": "Technical Interview (x2)", "icon": "💡", "desc": "Two rounds: one DSA-focused, one on your tech stack (React/Java/Python).", "prep": "Review system design basics and your framework deeply."},
            {"name": "Behavioural Round", "icon": "🎭", "desc": "STAR-format questions on teamwork, conflict, leadership.", "prep": "Prepare 6–8 STAR stories covering different competencies."},
            {"name": "Final / Manager Round", "icon": "🏢", "desc": "Culture fit, long-term goals, team match discussion.", "prep": "Know why you want THIS company specifically. Have 3 good questions ready."},
        ]
    },
    "mid": {
        "label": "Mid-Level Engineer (3–6 yrs)",
        "stages": [
            {"name": "Coding Assessment", "icon": "⌨️", "desc": "Medium to hard problems. 2–3 questions in 2 hours.", "prep": "Focus on medium-hard LeetCode, DP, graphs, and system-level thinking."},
            {"name": "System Design Interview", "icon": "🏗️", "desc": "Design a scalable system: URL shortener, Twitter feed, Uber, etc.", "prep": "Study 'Designing Data-Intensive Applications'. Practice 10 system designs."},
            {"name": "Technical Deep Dive", "icon": "🔭", "desc": "Architecture of past projects, trade-offs, debugging scenarios.", "prep": "Be ready to whiteboard your last 3 major projects and their trade-offs."},
            {"name": "Behavioural / Leadership", "icon": "🎯", "desc": "Own team impact, mentoring, cross-team collaboration.", "prep": "Show ownership. Companies want builders, not just coders."},
            {"name": "Bar Raiser / Hiring Manager", "icon": "📋", "desc": "Final round checking culture, ambition, long-term fit.", "prep": "Know the company's product deeply. Have 5 smart questions ready."},
        ]
    },
    "senior": {
        "label": "Senior / Lead Engineer (6+ yrs)",
        "stages": [
            {"name": "System Design (2 rounds)", "icon": "🏗️", "desc": "Large-scale distributed systems. Consensus, sharding, CAP theorem.", "prep": "Practice 20+ system design problems. Read 'DDIA' book fully."},
            {"name": "Coding (Advanced)", "icon": "⌨️", "desc": "Hard leetcode. Focus on optimization, complexity analysis.", "prep": "Solve 100+ hard problems. Explain trade-offs clearly."},
            {"name": "Leadership & Execution", "icon": "🚀", "desc": "How you drove projects, made decisions, unblocked teams.", "prep": "Have 10+ impactful leadership stories. Quantify everything."},
            {"name": "Cross-functional Influence", "icon": "🌐", "desc": "Working with product, design, data teams. Stakeholder management.", "prep": "Show breadth: you've influenced roadmaps, not just written code."},
            {"name": "VP / Director Round", "icon": "🏛️", "desc": "Strategic thinking, vision alignment, company growth mindset.", "prep": "Research company strategy and OKRs. Align your vision with theirs."},
        ]
    },
}


def get_interview_track(exp_years, jd_text="", skills=None):
    """Determine interview track based on experience and skills."""
    if exp_years == 0:
        return INTERVIEW_STAGES["freshers"]
    elif exp_years <= 3:
        return INTERVIEW_STAGES["junior"]
    elif exp_years <= 6:
        return INTERVIEW_STAGES["mid"]
    else:
        return INTERVIEW_STAGES["senior"]


def match_companies(skills, exp_years, target_role="", preferred_type=""):
    """Score and rank companies based on candidate profile."""
    skill_lower = [s.lower() for s in skills]
    jd_lower = target_role.lower()
    scored = []
    for company in COMPANY_DATABASE:
        match_score = 0
        for domain_kw in company["domain"]:
            if any(domain_kw in s for s in skill_lower):
                match_score += 10
            if domain_kw in jd_lower:
                match_score += 5
        # Adjust for experience level
        if exp_years == 0 and company["type"] == "Service":
            match_score += 15  # freshers → services
        elif exp_years >= 4 and company["type"] == "Product":
            match_score += 10
        elif exp_years >= 2 and company["type"] == "Startup":
            match_score += 8
        # Type preference
        if preferred_type and preferred_type.lower() in company["type"].lower():
            match_score += 20
        if match_score > 0:
            scored.append({**company, "match_score": match_score})
    scored.sort(key=lambda x: x["match_score"], reverse=True)
    return scored[:5]


# ── Text extraction ──
def extract_text_from_pdf(file_path):
    text_parts = []
    pdf = fitz.open(file_path)
    for page in pdf:
        t = page.get_text("text")
        text_parts.append(t if isinstance(t, str) else "")
    return " ".join(text_parts)


def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return " ".join([p.text for p in doc.paragraphs])


def read_resume(file_path):
    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        return extract_text_from_docx(file_path)
    return ""


def get_similarity(job_desc, resume_text):
    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform([job_desc, resume_text])
    dense = cast(Any, vectors).toarray()
    score = cosine_similarity(dense[0:1], dense[1:2])
    return round(float(score[0][0]) * 100, 2)


def extract_skills(text):
    text_lower = text.lower()
    found = []
    for skill in SKILL_KEYWORDS:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found.append(skill.title() if len(skill) <= 3 else skill.capitalize())
    return list(dict.fromkeys(found))


def extract_top_keywords(text, top_n=15):
    words = re.findall(r'\b[a-zA-Z][a-zA-Z+#.]{2,}\b', text.lower())
    filtered = [w for w in words if w not in STOP_WORDS and len(w) > 3]
    counter = Counter(filtered)
    return [word for word, _ in counter.most_common(top_n)]


def keyword_overlap(jd_keywords, resume_text):
    text_lower = resume_text.lower()
    matched = [kw for kw in jd_keywords if re.search(r'\b' + re.escape(kw) + r'\b', text_lower)]
    missing = [kw for kw in jd_keywords if kw not in matched]
    return matched, missing


def word_count(text):
    return len(text.split())


def extract_experience_years(text):
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


def count_action_verbs(text):
    text_lower = text.lower()
    found = [v for v in ACTION_VERBS if re.search(r'\b' + v + r'\b', text_lower)]
    return len(found), found


def has_quantified_achievements(text):
    pattern = r'(?:reduced|improved|increased|decreased|saved|grew|achieved|delivered|boosted)[^.\n]{0,60}\d+[%x]'
    return bool(re.search(pattern, text.lower()))


def detect_education(text):
    text_lower = text.lower()
    if any(k in text_lower for k in ['phd', 'ph.d', 'doctorate', 'doctor of']):
        return 'PhD'
    if any(k in text_lower for k in ['m.tech', 'mtech', 'm.e.', 'mba', 'master']):
        return 'Masters'
    if any(k in text_lower for k in ['b.tech', 'btech', 'b.e.', 'b.sc', 'bachelor', 'undergraduate']):
        return 'Bachelors'
    if any(k in text_lower for k in ['diploma', 'polytechnic']):
        return 'Diploma'
    return 'Unknown'


def generate_improvement_tips(result_data, jd_text):
    tips = []
    score = result_data.get('score', 0)
    ats  = result_data.get('ats_score', 0)
    wc   = result_data.get('word_count', 0)
    action_count = result_data.get('action_verb_count', 0)
    has_quant    = result_data.get('has_quantified', False)
    missing_skills = result_data.get('missing_skills', [])
    missing_kw     = result_data.get('missing_keywords', [])
    ats_details    = result_data.get('ats_details', {})

    if missing_skills:
        top_missing = ', '.join(missing_skills[:3])
        tips.append({'icon': '🎯', 'text': f'Add missing skills: <strong>{top_missing}</strong> — these appear in the job description.'})
    if not has_quant:
        tips.append({'icon': '📊', 'text': 'Add <strong>quantified achievements</strong> — e.g. "Reduced API latency by 35%" or "Shipped 3 features in Q2".' })
    if action_count < 5:
        tips.append({'icon': '✍️', 'text': 'Use stronger <strong>action verbs</strong> to start bullet points (e.g. Architected, Optimized, Delivered, Shipped).'})
    if wc < 300:
        tips.append({'icon': '📝', 'text': f'Resume is too short ({wc} words). Expand experience bullets and add a project or summary section.'})
    elif wc > 900:
        tips.append({'icon': '✂️', 'text': f'Resume is too long ({wc} words). Trim to 400–700 words for optimal ATS readability.'})
    if not ats_details.get('contact', {}).get('linkedin'):
        tips.append({'icon': '🔗', 'text': 'Add a <strong>LinkedIn profile URL</strong> — most ATS systems and recruiters expect it.'})
    if not ats_details.get('contact', {}).get('email'):
        tips.append({'icon': '📧', 'text': 'No email address detected — make sure your contact info is in plain text, not inside an image or table.'})
    missing_sections = ats_details.get('sections', {}).get('missing', [])
    if 'summary' in missing_sections:
        tips.append({'icon': '💡', 'text': 'Add a <strong>Professional Summary</strong> section — 2–3 lines tailored to this specific role.'})
    if 'experience' in missing_sections:
        tips.append({'icon': '🏢', 'text': 'Add a clear <strong>Work Experience</strong> section header so ATS can parse your employment history.'})
    if missing_kw:
        top_kw = ', '.join(missing_kw[:4])
        tips.append({'icon': '🔑', 'text': f'Include missing keywords from the JD: <strong>{top_kw}</strong>.'})
    if score < 40:
        tips.append({'icon': '🔄', 'text': 'Consider tailoring this resume specifically for this role — a generic resume scores much lower.'})
    if ats < 50:
        tips.append({'icon': '🤖', 'text': 'Low ATS score — avoid columns, graphics, or tables. Use a clean single-column layout.'})
    return tips[:6]


def get_strength(score):
    if score >= 75:
        return {"label": "Excellent Match", "color": "emerald", "emoji": "🏆", "tier": "A"}
    elif score >= 55:
        return {"label": "Strong Match", "color": "cyan", "emoji": "✅", "tier": "B"}
    elif score >= 35:
        return {"label": "Moderate Match", "color": "amber", "emoji": "🟡", "tier": "C"}
    else:
        return {"label": "Weak Match", "color": "rose", "emoji": "🔴", "tier": "D"}


def compute_ats_score(resume_text):
    text_lower = resume_text.lower()
    checks = {}
    total = 0
    possible = 0

    sections = {
        "experience": ["experience", "work experience", "employment", "professional experience"],
        "education":  ["education", "academic", "qualification", "degree"],
        "skills":     ["skills", "technical skills", "core competencies", "technologies"],
        "summary":    ["summary", "objective", "profile", "about me", "overview"],
    }
    found_sections = []
    for sec, keywords in sections.items():
        if any(k in text_lower for k in keywords):
            found_sections.append(sec)
            total += 6
        possible += 6
    checks["sections"] = {
        "found": found_sections,
        "missing": [s for s in sections if s not in found_sections],
        "score": len(found_sections) * 6,
        "max": 24,
    }

    has_email = bool(re.search(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', resume_text))
    has_phone = bool(re.search(r'(\+?\d[\d\s\-\(\)]{7,14}\d)', resume_text))
    has_linkedin = "linkedin" in text_lower
    contact_score = (8 if has_email else 0) + (7 if has_phone else 0) + (5 if has_linkedin else 0)
    total += contact_score
    possible += 20
    checks["contact"] = {
        "email": has_email, "phone": has_phone, "linkedin": has_linkedin,
        "score": contact_score, "max": 20,
    }

    date_patterns = [
        r'\b(19|20)\d{2}\b',
        r'\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s+(19|20)\d{2}\b',
        r'\b(0?[1-9]|1[0-2])\s*/\s*(19|20)\d{2}\b',
    ]
    has_dates = any(re.search(p, text_lower) for p in date_patterns)
    total += 20 if has_dates else 0
    possible += 20
    checks["dates"] = {"found": has_dates, "score": 20 if has_dates else 0, "max": 20}

    wc = word_count(resume_text)
    if 300 <= wc <= 700:
        len_score = 20; len_note = "Ideal length"
    elif 200 <= wc < 300 or 700 < wc <= 900:
        len_score = 12; len_note = "Slightly short" if wc < 300 else "Slightly long"
    elif wc < 200:
        len_score = 4; len_note = "Too short"
    else:
        len_score = 6; len_note = "Too long"
    total += len_score
    possible += 20
    checks["length"] = {"word_count": wc, "score": len_score, "max": 20, "note": len_note}

    words = resume_text.split()
    avg_word_len = sum(len(w) for w in words) / max(len(words), 1)
    good_format = avg_word_len < 14
    total += 16 if good_format else 0
    possible += 16
    checks["formatting"] = {
        "parseable": good_format,
        "score": 16 if good_format else 0,
        "max": 16,
        "note": "Text parsed cleanly" if good_format else "Possible table/column layout — may confuse ATS",
    }

    ats_score = round((total / possible) * 100) if possible > 0 else 0
    return ats_score, checks


# ── Main screener view ──
def screener(request):
    results = []
    jd_keywords = []
    jd_skills = []
    jd_word_count = 0
    resume_count = 0
    session = None
    interview_track = None
    matched_companies = []
    candidate_info = {}

    if request.method == "POST":
        job_desc = request.POST.get("job_description", "").strip()
        files = request.FILES.getlist("resumes")

        # ── Candidate profile fields ──
        candidate_name = request.POST.get("candidate_name", "").strip()
        candidate_email = request.POST.get("candidate_email", "").strip()
        target_role = request.POST.get("target_role", "").strip()
        experience_level = request.POST.get("experience_level", "").strip()
        manual_exp_years = request.POST.get("exp_years", "0").strip()
        preferred_company_type = request.POST.get("preferred_company_type", "").strip()
        candidate_location = request.POST.get("candidate_location", "").strip()
        notice_period = request.POST.get("notice_period", "").strip()
        current_ctc = request.POST.get("current_ctc", "").strip()
        expected_ctc = request.POST.get("expected_ctc", "").strip()
        candidate_summary = request.POST.get("candidate_summary", "").strip()

        candidate_info = {
            "name": candidate_name,
            "email": candidate_email,
            "target_role": target_role,
            "experience_level": experience_level,
            "exp_years": int(manual_exp_years) if manual_exp_years.isdigit() else 0,
            "preferred_company_type": preferred_company_type,
            "location": candidate_location,
            "notice_period": notice_period,
            "current_ctc": current_ctc,
            "expected_ctc": expected_ctc,
            "summary": candidate_summary,
        }

        if job_desc:
            jd_keywords = extract_top_keywords(job_desc, top_n=20)
            jd_skills = extract_skills(job_desc)
            jd_word_count = word_count(job_desc)

        for file in files:
            if not file:
                continue
            original_name = file.name or ""
            safe_name = secure_filename(original_name)
            if not safe_name:
                continue

            file_path = os.path.join(UPLOAD_DIR, safe_name)
            with open(file_path, 'wb+') as dest:
                for chunk in file.chunks():
                    dest.write(chunk)

            resume_text = read_resume(file_path)
            score = get_similarity(job_desc, resume_text) if job_desc else 0

            resume_skills = extract_skills(resume_text)
            matched_kw, missing_kw = keyword_overlap(jd_keywords, resume_text)
            matched_skills = [s for s in jd_skills if s.lower() in resume_text.lower()]
            missing_skills = [s for s in jd_skills if s.lower() not in resume_text.lower()]

            kw_score = round(len(matched_kw) / max(len(jd_keywords), 1) * 100)
            skill_score = round(len(matched_skills) / max(len(jd_skills), 1) * 100) if jd_skills else score
            wc = word_count(resume_text)

            ats_score, ats_details = compute_ats_score(resume_text)

            exp_years = extract_experience_years(resume_text)
            if candidate_info["exp_years"] > 0:
                exp_years = candidate_info["exp_years"]

            action_count, action_verbs_found = count_action_verbs(resume_text)
            has_quant = has_quantified_achievements(resume_text)
            education = detect_education(resume_text)

            strength = get_strength(score)

            result_entry = {
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
                "candidate_info": candidate_info,
            }

            result_entry["improvement_tips"] = generate_improvement_tips(result_entry, job_desc)
            results.append(result_entry)

        results = sorted(results, key=lambda x: x["score"], reverse=True)
        resume_count = len(results)

        # Determine interview track from best resume or manual input
        if results or candidate_info.get("exp_years", 0) > 0:
            exp_for_track = candidate_info.get("exp_years", 0)
            if not exp_for_track and results:
                exp_for_track = results[0].get("experience_years", 0)
            interview_track = get_interview_track(exp_for_track, job_desc)

        # Company matching — use all detected skills
        all_skills = []
        if results:
            for r in results:
                all_skills.extend(r.get("resume_skills", []))
        all_skills = list(dict.fromkeys(all_skills))
        exp_for_match = candidate_info.get("exp_years", 0) or (results[0].get("experience_years", 0) if results else 0)
        matched_companies = match_companies(all_skills, exp_for_match, target_role, preferred_company_type)

        # Save session to DB
        if results and job_desc:
            session = ScreeningSession.objects.create(
                job_description=job_desc,
                jd_word_count=jd_word_count,
                resume_count=resume_count,
            )
            for rank, r in enumerate(results, 1):
                ResumeResult.objects.create(
                    session=session, rank=rank,
                    filename=r["name"], score=r["score"],
                    strength_label=r["strength"]["label"],
                    strength_color=r["strength"]["color"],
                    strength_emoji=r["strength"]["emoji"],
                    strength_tier=r["strength"]["tier"],
                    resume_skills=r["resume_skills"],
                    matched_keywords=r["matched_keywords"],
                    missing_keywords=r["missing_keywords"],
                    matched_skills=r["matched_skills"],
                    missing_skills=r["missing_skills"],
                    kw_score=r["kw_score"],
                    skill_score=r["skill_score"],
                    word_count=r["word_count"],
                    ats_score=r["ats_score"],
                    ats_details=r["ats_details"],
                )

    detected_skills_json = "[]"
    if results:
        all_detected = []
        for r in results:
            all_detected.extend(r.get("resume_skills", []))
        unique_skills = list(dict.fromkeys(all_detected))[:10]
        detected_skills_json = json.dumps(unique_skills)

    return render(request, 'resume_screener/screener.html', {
        'results': results,
        'jd_keywords': jd_keywords,
        'jd_skills': jd_skills,
        'jd_word_count': jd_word_count,
        'resume_count': resume_count,
        'session': session,
        'detected_skills_json': detected_skills_json,
        'interview_track': interview_track,
        'matched_companies': matched_companies,
        'candidate_info': candidate_info,
        'chart_labels_json': json.dumps([r["name"][:20] for r in results]),
        'chart_scores_json': json.dumps([r["score"] for r in results]),
        'chart_ats_json': json.dumps([r["ats_score"] for r in results]),
    })


def screener_history(request):
    sessions = ScreeningSession.objects.prefetch_related('results').all()
    return render(request, 'resume_screener/screener_history.html', {'sessions': sessions})


@require_http_methods(['POST'])
def delete_session(request, pk):
    session = get_object_or_404(ScreeningSession, pk=pk)
    session.delete()
    return redirect('screener_history')


def shared_session(request, token):
    session = get_object_or_404(ScreeningSession, share_token=token)
    results = []
    for r in session.results.all():
        results.append({
            "name": r.filename, "score": r.score,
            "strength": {"label": r.strength_label, "color": r.strength_color, "emoji": r.strength_emoji, "tier": r.strength_tier},
            "resume_skills": r.resume_skills,
            "matched_keywords": r.matched_keywords,
            "missing_keywords": r.missing_keywords,
            "matched_skills": r.matched_skills,
            "missing_skills": r.missing_skills,
            "kw_score": r.kw_score, "skill_score": r.skill_score,
            "word_count": r.word_count, "ats_score": r.ats_score, "ats_details": r.ats_details,
        })

    jd_keywords = extract_top_keywords(session.job_description, top_n=12)
    jd_skills = extract_skills(session.job_description)

    return render(request, 'resume_screener/screener.html', {
        'results': results, 'jd_keywords': jd_keywords, 'jd_skills': jd_skills,
        'jd_word_count': session.jd_word_count, 'resume_count': session.resume_count,
        'session': session, 'is_shared_view': True, 'detected_skills_json': '[]',
        'interview_track': None, 'matched_companies': [], 'candidate_info': {},
        'chart_labels_json': json.dumps([r["name"][:20] for r in results]),
        'chart_scores_json': json.dumps([r["score"] for r in results]),
        'chart_ats_json': json.dumps([r["ats_score"] for r in results]),
    })


def download_report(request, token):
    session = get_object_or_404(ScreeningSession, share_token=token)
    results = session.results.order_by('rank')

    try:
        import fitz as _fitz

        doc = _fitz.open()
        MARGIN = 50
        PAGE_W, PAGE_H = 595, 842

        C_BRAND   = (0.318, 0.42, 0.925)
        C_EMERALD = (0.204, 0.831, 0.6)
        C_AMBER   = (0.98, 0.749, 0.141)
        C_ROSE    = (0.984, 0.443, 0.522)
        C_CYAN    = (0.133, 0.827, 0.933)
        C_DARK    = (0.059, 0.078, 0.118)
        C_MID     = (0.58, 0.639, 0.722)
        C_LIGHT   = (0.945, 0.961, 0.988)
        C_WHITE   = (1, 1, 1)

        def new_page(doc):
            page = doc.new_page(width=PAGE_W, height=PAGE_H)
            page.draw_rect(_fitz.Rect(0, 0, PAGE_W, PAGE_H), color=None, fill=C_DARK)
            return page

        def strength_color(tier):
            return {"A": C_EMERALD, "B": C_CYAN, "C": C_AMBER, "D": C_ROSE}.get(tier, C_MID)

        page = new_page(doc)
        page.draw_rect(_fitz.Rect(0, 0, PAGE_W, 120), color=None, fill=(0.07, 0.09, 0.22))
        page.draw_line(_fitz.Point(0, 120), _fitz.Point(PAGE_W, 120), color=C_BRAND, width=2)
        page.insert_text((MARGIN, 52), "CareerCompass", fontsize=22, color=C_WHITE, fontname="helv")
        page.insert_text((MARGIN, 80), "Resume Screening Report", fontsize=13, color=C_MID, fontname="helv")

        y = 148
        jd_preview = (session.job_description[:200] + "...") if len(session.job_description) > 200 else session.job_description
        page.insert_text((MARGIN, y), "Job Description (preview):", fontsize=9, color=C_MID, fontname="helv")
        y += 18
        words = jd_preview.split()
        line, lines = [], []
        for w in words:
            line.append(w)
            if len(" ".join(line)) > 85:
                lines.append(" ".join(line[:-1]))
                line = [w]
        if line:
            lines.append(" ".join(line))
        for l in lines[:6]:
            page.insert_text((MARGIN, y), l, fontsize=9, color=C_LIGHT, fontname="helv")
            y += 14

        y += 12
        stats = [
            ("Resumes Screened", str(session.resume_count)),
            ("Screening Date", session.created_at.strftime("%d %b %Y, %I:%M %p")),
            ("Top Score", f"{results.first().score:.1f}%" if results.exists() else "—"),
        ]
        for label, val in stats:
            page.insert_text((MARGIN, y), f"{label}:", fontsize=9, color=C_MID, fontname="helv")
            page.insert_text((220, y), val, fontsize=9, color=C_WHITE, fontname="helv")
            y += 18

        y += 20
        page.draw_line(_fitz.Point(MARGIN, y), _fitz.Point(PAGE_W - MARGIN, y), color=C_BRAND, width=0.5)
        y += 14
        page.insert_text((MARGIN, y), "Ranked Results", fontsize=13, color=C_WHITE, fontname="helv")
        y += 22

        cols = [MARGIN, 80, 240, 330, 420, 480]
        headers = ["#", "Filename", "Match", "Grade", "ATS", "Keywords"]
        for i, h in enumerate(headers):
            page.insert_text((cols[i], y), h, fontsize=8, color=C_MID, fontname="helv")
        y += 4
        page.draw_line(_fitz.Point(MARGIN, y + 4), _fitz.Point(PAGE_W - MARGIN, y + 4), color=(0.2, 0.23, 0.38), width=0.5)
        y += 14

        for r in results:
            if y > PAGE_H - 80:
                page = new_page(doc)
                y = 80
            sc = strength_color(r.strength_tier)
            row_data = [str(r.rank), r.filename[:28], f"{r.score:.1f}%", r.strength_tier, f"{r.ats_score}%", f"{len(r.matched_keywords)}/{len(r.matched_keywords) + len(r.missing_keywords)}"]
            for i, val in enumerate(row_data):
                color = sc if i in (2, 3) else C_LIGHT
                page.insert_text((cols[i], y), val, fontsize=8, color=color, fontname="helv")
            y += 16

        for r in results:
            page = new_page(doc)
            page.draw_rect(_fitz.Rect(0, 0, PAGE_W, 90), color=None, fill=(0.07, 0.09, 0.22))
            sc = strength_color(r.strength_tier)
            page.draw_line(_fitz.Point(0, 90), _fitz.Point(PAGE_W, 90), color=sc, width=2)
            page.insert_text((MARGIN, 34), f"#{r.rank}  {r.filename}", fontsize=14, color=C_WHITE, fontname="helv")
            page.insert_text((MARGIN, 58), f"{r.strength_emoji}  {r.strength_label}", fontsize=10, color=sc, fontname="helv")
            page.insert_text((PAGE_W - 110, 38), f"{r.score:.1f}%", fontsize=22, color=sc, fontname="helv")
            page.insert_text((PAGE_W - 110, 62), "Similarity", fontsize=8, color=C_MID, fontname="helv")

            y = 116
            def section(title):
                nonlocal y
                page.insert_text((MARGIN, y), title, fontsize=9, color=C_MID, fontname="helv")
                y += 4
                page.draw_line(_fitz.Point(MARGIN, y + 4), _fitz.Point(PAGE_W - MARGIN, y + 4), color=(0.2, 0.23, 0.38), width=0.4)
                y += 16

            section("Score Breakdown")
            bars = [("Similarity", r.score, C_BRAND), ("ATS Score", r.ats_score, C_EMERALD), ("Keyword Coverage", r.kw_score, C_CYAN), ("Skill Match", r.skill_score, C_AMBER)]
            BAR_W = 340
            for label, val, color in bars:
                page.insert_text((MARGIN, y), label + ":", fontsize=8, color=C_MID, fontname="helv")
                page.insert_text((200, y), f"{val:.0f}%", fontsize=8, color=C_WHITE, fontname="helv")
                fill_w = max(4, int(BAR_W * min(val, 100) / 100))
                page.draw_rect(_fitz.Rect(MARGIN, y + 4, MARGIN + BAR_W, y + 10), color=None, fill=(0.2, 0.23, 0.38))
                page.draw_rect(_fitz.Rect(MARGIN, y + 4, MARGIN + fill_w, y + 10), color=None, fill=color)
                y += 22

            y += 6
            section("Matched Skills")
            skills_line = "  ".join(r.matched_skills[:12]) if r.matched_skills else "None"
            page.insert_text((MARGIN, y), skills_line, fontsize=8, color=C_EMERALD, fontname="helv")
            y += 18

            section("Missing Skills")
            missing_line = "  ".join(r.missing_skills[:12]) if r.missing_skills else "None"
            page.insert_text((MARGIN, y), missing_line, fontsize=8, color=C_ROSE, fontname="helv")
            y += 18

            page.draw_line(_fitz.Point(MARGIN, PAGE_H - 40), _fitz.Point(PAGE_W - MARGIN, PAGE_H - 40), color=(0.2, 0.23, 0.38), width=0.4)
            page.insert_text((MARGIN, PAGE_H - 24), "Generated by CareerCompass — AI-Powered Career Guidance", fontsize=7, color=C_MID, fontname="helv")

        pdf_bytes = doc.tobytes()
        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="screening_report_{session.share_token}.pdf"'
        return response

    except Exception as e:
        return HttpResponse(f"PDF generation failed: {e}", status=500)


def api_extract_skills(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    files = request.FILES.getlist("resume")
    if not files:
        return JsonResponse({"error": "No file uploaded"}, status=400)

    file = files[0]
    safe_name = secure_filename(file.name or "resume")
    if not safe_name:
        return JsonResponse({"error": "Invalid filename"}, status=400)

    file_path = os.path.join(UPLOAD_DIR, safe_name)
    with open(file_path, 'wb+') as dest:
        for chunk in file.chunks():
            dest.write(chunk)

    resume_text = read_resume(file_path)
    detected_skills = extract_skills(resume_text)

    from careers.career_engine import SKILLS_LIST as CAREER_SKILLS
    career_skill_lower = {s.lower(): s for s in CAREER_SKILLS}
    matched_career_skills = []
    for skill in detected_skills:
        key = skill.lower()
        if key in career_skill_lower:
            matched_career_skills.append(career_skill_lower[key])

    return JsonResponse({
        "all_detected": detected_skills,
        "career_skills": matched_career_skills,
        "resume_preview": resume_text[:300],
    })
