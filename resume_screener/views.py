import os
import re
from typing import Any, cast
from collections import Counter

import fitz  # PyMuPDF
import docx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from werkzeug.utils import secure_filename

from django.shortcuts import render
from django.conf import settings


# ── Upload folder ──
UPLOAD_DIR = os.path.join(settings.BASE_DIR, 'resume_screener', 'uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ── Common tech skills / keywords for extraction ──
SKILL_KEYWORDS = [
    # Languages
    "python","java","javascript","typescript","c++","c#","golang","rust","swift","kotlin","php","ruby","scala","r",
    # Web
    "react","vue","angular","next.js","node.js","django","flask","fastapi","spring","html","css","tailwind","bootstrap",
    # Data / ML
    "machine learning","deep learning","tensorflow","pytorch","keras","scikit-learn","pandas","numpy","matplotlib",
    "data analysis","nlp","computer vision","sql","mysql","postgresql","mongodb","redis","elasticsearch",
    # Cloud / DevOps
    "aws","azure","gcp","docker","kubernetes","ci/cd","jenkins","github actions","terraform","ansible","linux",
    # Tools
    "git","rest api","graphql","microservices","agile","scrum","jira","figma","excel","power bi","tableau",
    # Soft
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


# ── TF-IDF cosine similarity ──
def get_similarity(job_desc, resume_text):
    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform([job_desc, resume_text])
    dense = cast(Any, vectors).toarray()
    score = cosine_similarity(dense[0:1], dense[1:2])
    return round(float(score[0][0]) * 100, 2)


# ── Extract skill keywords from text ──
def extract_skills(text):
    text_lower = text.lower()
    found = []
    for skill in SKILL_KEYWORDS:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found.append(skill.title() if len(skill) <= 3 else skill.capitalize())
    return list(dict.fromkeys(found))  # deduplicate, preserve order


# ── Extract top keywords from a text ──
def extract_top_keywords(text, top_n=15):
    words = re.findall(r'\b[a-zA-Z][a-zA-Z+#.]{2,}\b', text.lower())
    filtered = [w for w in words if w not in STOP_WORDS and len(w) > 3]
    counter = Counter(filtered)
    return [word for word, _ in counter.most_common(top_n)]


# ── Keyword overlap between JD and resume ──
def keyword_overlap(jd_keywords, resume_text):
    text_lower = resume_text.lower()
    matched = [kw for kw in jd_keywords if re.search(r'\b' + re.escape(kw) + r'\b', text_lower)]
    missing = [kw for kw in jd_keywords if kw not in matched]
    return matched, missing


# ── Estimate word count and read time ──
def word_count(text):
    return len(text.split())


# ── Strength label ──
def get_strength(score):
    if score >= 75:
        return {"label": "Excellent Match", "color": "emerald", "emoji": "🏆", "tier": "A"}
    elif score >= 55:
        return {"label": "Strong Match", "color": "cyan", "emoji": "✅", "tier": "B"}
    elif score >= 35:
        return {"label": "Moderate Match", "color": "amber", "emoji": "🟡", "tier": "C"}
    else:
        return {"label": "Weak Match", "color": "rose", "emoji": "🔴", "tier": "D"}


# ── Main view ──
def screener(request):
    results = []
    jd_keywords = []
    jd_skills = []
    jd_word_count = 0
    resume_count = 0

    if request.method == "POST":
        job_desc = request.POST.get("job_description", "").strip()
        files = request.FILES.getlist("resumes")

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
            score = get_similarity(job_desc, resume_text)

            resume_skills = extract_skills(resume_text)
            matched_kw, missing_kw = keyword_overlap(jd_keywords, resume_text)
            matched_skills = [s for s in jd_skills if s.lower() in resume_text.lower()]
            missing_skills = [s for s in jd_skills if s.lower() not in resume_text.lower()]

            # per-component scores (approximate breakdown)
            kw_score = round(len(matched_kw) / max(len(jd_keywords), 1) * 100)
            skill_score = round(len(matched_skills) / max(len(jd_skills), 1) * 100) if jd_skills else score
            wc = word_count(resume_text)

            strength = get_strength(score)

            results.append({
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
            })

        results = sorted(results, key=lambda x: x["score"], reverse=True)
        resume_count = len(results)

    return render(request, 'resume_screener/screener.html', {
        'results': results,
        'jd_keywords': jd_keywords,
        'jd_skills': jd_skills,
        'jd_word_count': jd_word_count,
        'resume_count': resume_count,
    })
