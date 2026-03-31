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
    return list(dict.fromkeys(found))


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


# ── Estimate word count ──
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


# ── Feature 3: ATS Score Simulation ──
def compute_ats_score(resume_text):
    """
    Simulate an ATS scan. Returns (score 0-100, details dict).
    Checks: standard sections, contact info, dates, length, table/column detection.
    """
    text_lower = resume_text.lower()
    checks = {}
    total = 0
    possible = 0

    # 1. Standard sections (25 pts)
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

    # 2. Contact info (20 pts)
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

    # 3. Dates in work history (20 pts)
    date_patterns = [
        r'\b(19|20)\d{2}\b',
        r'\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s+(19|20)\d{2}\b',
        r'\b(0?[1-9]|1[0-2])\s*/\s*(19|20)\d{2}\b',
    ]
    has_dates = any(re.search(p, text_lower) for p in date_patterns)
    total += 20 if has_dates else 0
    possible += 20
    checks["dates"] = {"found": has_dates, "score": 20 if has_dates else 0, "max": 20}

    # 4. Resume length (20 pts — ideal 300-700 words)
    wc = word_count(resume_text)
    if 300 <= wc <= 700:
        len_score = 20
        len_note = "Ideal length"
    elif 200 <= wc < 300 or 700 < wc <= 900:
        len_score = 12
        len_note = "Slightly short" if wc < 300 else "Slightly long"
    elif wc < 200:
        len_score = 4
        len_note = "Too short"
    else:
        len_score = 6
        len_note = "Too long"
    total += len_score
    possible += 20
    checks["length"] = {"word_count": wc, "score": len_score, "max": 20, "note": len_note}

    # 5. Formatting signal — detect garbled column text (16 pts)
    # Heuristic: if avg word length > 15, likely garbled from column extraction
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

            kw_score = round(len(matched_kw) / max(len(jd_keywords), 1) * 100)
            skill_score = round(len(matched_skills) / max(len(jd_skills), 1) * 100) if jd_skills else score
            wc = word_count(resume_text)

            # Feature 3: ATS score
            ats_score, ats_details = compute_ats_score(resume_text)

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
                "ats_score": ats_score,
                "ats_details": ats_details,
            })

        results = sorted(results, key=lambda x: x["score"], reverse=True)
        resume_count = len(results)

        # Feature 2: Save session to DB
        if results and job_desc:
            session = ScreeningSession.objects.create(
                job_description=job_desc,
                jd_word_count=jd_word_count,
                resume_count=resume_count,
            )
            for rank, r in enumerate(results, 1):
                ResumeResult.objects.create(
                    session=session,
                    rank=rank,
                    filename=r["name"],
                    score=r["score"],
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

    # Feature 1: Build auto-fill URL for career form
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
        # Feature 6: chart data
        'chart_labels_json': json.dumps([r["name"][:20] for r in results]),
        'chart_scores_json': json.dumps([r["score"] for r in results]),
        'chart_ats_json': json.dumps([r["ats_score"] for r in results]),
    })


# Feature 2: Screening history view
def screener_history(request):
    sessions = ScreeningSession.objects.prefetch_related('results').all()
    return render(request, 'resume_screener/screener_history.html', {'sessions': sessions})


# Feature 2: Delete session
@require_http_methods(['POST'])
def delete_session(request, pk):
    session = get_object_or_404(ScreeningSession, pk=pk)
    session.delete()
    return redirect('screener_history')


# Feature 5: Shared screening result (read-only via UUID)
def shared_session(request, token):
    session = get_object_or_404(ScreeningSession, share_token=token)
    results = []
    for r in session.results.all():
        results.append({
            "name": r.filename,
            "score": r.score,
            "strength": {
                "label": r.strength_label,
                "color": r.strength_color,
                "emoji": r.strength_emoji,
                "tier": r.strength_tier,
            },
            "resume_skills": r.resume_skills,
            "matched_keywords": r.matched_keywords,
            "missing_keywords": r.missing_keywords,
            "matched_skills": r.matched_skills,
            "missing_skills": r.missing_skills,
            "kw_score": r.kw_score,
            "skill_score": r.skill_score,
            "word_count": r.word_count,
            "ats_score": r.ats_score,
            "ats_details": r.ats_details,
        })

    jd_keywords = extract_top_keywords(session.job_description, top_n=12)
    jd_skills = extract_skills(session.job_description)
    share_url = request.build_absolute_uri(f'/screener/results/{session.share_token}/')

    return render(request, 'resume_screener/screener.html', {
        'results': results,
        'jd_keywords': jd_keywords,
        'jd_skills': jd_skills,
        'jd_word_count': session.jd_word_count,
        'resume_count': session.resume_count,
        'session': session,
        'share_url': share_url,
        'is_shared_view': True,
        'detected_skills_json': '[]',
        'chart_labels_json': json.dumps([r["name"][:20] for r in results]),
        'chart_scores_json': json.dumps([r["score"] for r in results]),
        'chart_ats_json': json.dumps([r["ats_score"] for r in results]),
    })


# Feature 4: Download PDF report
def download_report(request, token):
    session = get_object_or_404(ScreeningSession, share_token=token)
    results = session.results.order_by('rank')

    try:
        import fitz as _fitz

        doc = _fitz.open()
        MARGIN = 50
        PAGE_W, PAGE_H = 595, 842  # A4

        # ── colour palette ──
        C_BRAND   = (0.318, 0.42, 0.925)   # indigo
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

        # ── COVER PAGE ──
        page = new_page(doc)

        # Header bar
        page.draw_rect(_fitz.Rect(0, 0, PAGE_W, 120), color=None,
                       fill=(0.07, 0.09, 0.22))
        page.draw_line(_fitz.Point(0, 120), _fitz.Point(PAGE_W, 120),
                       color=C_BRAND, width=2)

        page.insert_text((MARGIN, 52), "🧭  CareerCompass",
                         fontsize=22, color=C_WHITE, fontname="helv")
        page.insert_text((MARGIN, 80), "Resume Screening Report",
                         fontsize=13, color=C_MID, fontname="helv")

        # Meta block
        y = 148
        jd_preview = (session.job_description[:200] + "…") if len(session.job_description) > 200 else session.job_description
        page.insert_text((MARGIN, y), "Job Description (preview):", fontsize=9, color=C_MID, fontname="helv")
        y += 18
        # Word-wrap the preview
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
            ("Screening Date",   session.created_at.strftime("%d %b %Y, %I:%M %p")),
            ("Top Score",        f"{results.first().score:.1f}%" if results.exists() else "—"),
        ]
        for label, val in stats:
            page.insert_text((MARGIN, y), f"{label}:", fontsize=9, color=C_MID, fontname="helv")
            page.insert_text((220, y), val, fontsize=9, color=C_WHITE, fontname="helv")
            y += 18

        # ── LEADERBOARD TABLE ──
        y += 20
        page.draw_line(_fitz.Point(MARGIN, y), _fitz.Point(PAGE_W - MARGIN, y),
                       color=C_BRAND, width=0.5)
        y += 14
        page.insert_text((MARGIN, y), "Ranked Results", fontsize=13, color=C_WHITE, fontname="helv")
        y += 22

        # Column headers
        cols = [MARGIN, 80, 240, 330, 420, 480]
        headers = ["#", "Filename", "Match", "Grade", "ATS", "Keywords"]
        for i, h in enumerate(headers):
            page.insert_text((cols[i], y), h, fontsize=8, color=C_MID, fontname="helv")
        y += 4
        page.draw_line(_fitz.Point(MARGIN, y + 4), _fitz.Point(PAGE_W - MARGIN, y + 4),
                       color=(0.2, 0.23, 0.38), width=0.5)
        y += 14

        for r in results:
            if y > PAGE_H - 80:
                page = new_page(doc)
                y = 80

            sc = strength_color(r.strength_tier)
            row_data = [
                str(r.rank),
                r.filename[:28],
                f"{r.score:.1f}%",
                r.strength_tier,
                f"{r.ats_score}%",
                f"{len(r.matched_keywords)}/{len(r.matched_keywords) + len(r.missing_keywords)}",
            ]
            for i, val in enumerate(row_data):
                color = sc if i in (2, 3) else C_LIGHT
                page.insert_text((cols[i], y), val, fontsize=8, color=color, fontname="helv")
            y += 16

        # ── INDIVIDUAL RESUME PAGES ──
        for r in results:
            page = new_page(doc)

            # Header bar
            page.draw_rect(_fitz.Rect(0, 0, PAGE_W, 90), color=None,
                           fill=(0.07, 0.09, 0.22))
            sc = strength_color(r.strength_tier)
            page.draw_line(_fitz.Point(0, 90), _fitz.Point(PAGE_W, 90), color=sc, width=2)

            page.insert_text((MARGIN, 34), f"#{r.rank}  {r.filename}",
                             fontsize=14, color=C_WHITE, fontname="helv")
            page.insert_text((MARGIN, 58),
                             f"{r.strength_emoji}  {r.strength_label}",
                             fontsize=10, color=sc, fontname="helv")
            page.insert_text((PAGE_W - 110, 38), f"{r.score:.1f}%",
                             fontsize=22, color=sc, fontname="helv")
            page.insert_text((PAGE_W - 110, 62), "Similarity",
                             fontsize=8, color=C_MID, fontname="helv")

            y = 116
            def section(title):
                nonlocal y
                page.insert_text((MARGIN, y), title, fontsize=9, color=C_MID, fontname="helv")
                y += 4
                page.draw_line(_fitz.Point(MARGIN, y + 4),
                               _fitz.Point(PAGE_W - MARGIN, y + 4),
                               color=(0.2, 0.23, 0.38), width=0.4)
                y += 16

            # Score breakdown
            section("Score Breakdown")
            bars = [
                ("Similarity", r.score, C_BRAND),
                ("ATS Score",  r.ats_score, C_EMERALD),
                ("Keyword Coverage", r.kw_score, C_CYAN),
                ("Skill Match", r.skill_score, C_AMBER),
            ]
            BAR_W = 340
            for label, val, color in bars:
                page.insert_text((MARGIN, y), label + ":", fontsize=8, color=C_MID, fontname="helv")
                page.insert_text((200, y), f"{val:.0f}%", fontsize=8, color=C_WHITE, fontname="helv")
                fill_w = max(4, int(BAR_W * min(val, 100) / 100))
                page.draw_rect(_fitz.Rect(MARGIN, y + 4, MARGIN + BAR_W, y + 10),
                               color=None, fill=(0.2, 0.23, 0.38))
                page.draw_rect(_fitz.Rect(MARGIN, y + 4, MARGIN + fill_w, y + 10),
                               color=None, fill=color)
                y += 22

            y += 6
            section("ATS Analysis")
            ad = r.ats_details
            checks_map = {
                "contact":    ("Contact info",    ad.get("contact",    {}).get("score", 0), 20),
                "sections":   ("Resume sections", ad.get("sections",   {}).get("score", 0), 24),
                "dates":      ("Work dates",      ad.get("dates",      {}).get("score", 0), 20),
                "length":     ("Length quality",  ad.get("length",     {}).get("score", 0), 20),
                "formatting": ("Formatting",      ad.get("formatting", {}).get("score", 0), 16),
            }
            for key, (label, score_v, max_v) in checks_map.items():
                pct = round(score_v / max_v * 100) if max_v else 0
                icon = "✓" if pct >= 60 else "✗"
                col  = C_EMERALD if pct >= 60 else C_ROSE
                page.insert_text((MARGIN, y), f"{icon}  {label}: {score_v}/{max_v}", fontsize=8, color=col, fontname="helv")
                if key == "length":
                    note = ad.get("length", {}).get("note", "")
                    if note:
                        page.insert_text((310, y), note, fontsize=7, color=C_MID, fontname="helv")
                elif key == "formatting":
                    note = ad.get("formatting", {}).get("note", "")
                    if note:
                        page.insert_text((310, y), note, fontsize=7, color=C_MID, fontname="helv")
                y += 15

            y += 6
            section("Matched Skills")
            skills_line = "  ".join(r.matched_skills[:12]) if r.matched_skills else "None"
            page.insert_text((MARGIN, y), skills_line, fontsize=8, color=C_EMERALD, fontname="helv")
            y += 18

            section("Missing Skills")
            missing_line = "  ".join(r.missing_skills[:12]) if r.missing_skills else "None"
            page.insert_text((MARGIN, y), missing_line, fontsize=8, color=C_ROSE, fontname="helv")
            y += 18

            # Footer
            page.draw_line(_fitz.Point(MARGIN, PAGE_H - 40),
                          _fitz.Point(PAGE_W - MARGIN, PAGE_H - 40),
                          color=(0.2, 0.23, 0.38), width=0.4)
            page.insert_text((MARGIN, PAGE_H - 24),
                            "Generated by CareerCompass — AI-Powered Career Guidance",
                            fontsize=7, color=C_MID, fontname="helv")

        pdf_bytes = doc.tobytes()
        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        response['Content-Disposition'] = (
            f'attachment; filename="screening_report_{session.share_token}.pdf"'
        )
        return response

    except Exception as e:
        return HttpResponse(f"PDF generation failed: {e}", status=500)


# Feature 1: API to extract skills from a resume (for career form auto-fill)
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

    # Map screener skill names back to career engine SKILLS_LIST names
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
