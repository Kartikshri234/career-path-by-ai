"""
resume_screener/views.py
Thin view layer — form handling, DB persistence, and rendering only.
All heavy logic lives in screener_service.py.
"""
import json

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods

from .models import ScreeningSession, ResumeResult
from . import screener_service as svc


# ── Screener (main form + results) ────────────────────────────────────────────

def screener(request):
    ctx = {
        'results': [],
        'jd_keywords': [],
        'jd_skills': [],
        'jd_word_count': 0,
        'resume_count': 0,
        'session': None,
        'interview_track': None,
        'matched_companies': [],
        'candidate_info': {},
        'chart_labels_json': '[]',
        'chart_scores_json': '[]',
        'chart_ats_json': '[]',
        'detected_skills_json': '[]',
    }

    if request.method != "POST":
        return render(request, 'resume_screener/screener.html', ctx)

    # ── Collect form data ──────────────────────────────────────────────────────
    job_desc = request.POST.get("job_description", "").strip()
    files    = request.FILES.getlist("resumes")

    candidate_info = {
        "name":       request.POST.get("candidate_name", "").strip(),
        "email":      request.POST.get("candidate_email", "").strip(),
        "target_role":request.POST.get("target_role", "").strip(),
        "exp_years":  int(request.POST.get("exp_years", "0") or 0),
        "preferred_company_type": request.POST.get("preferred_company_type", "").strip(),
    }

    # ── JD analysis ───────────────────────────────────────────────────────────
    jd_keywords = jd_skills = []
    jd_word_count = 0
    if job_desc:
        jd_keywords   = svc.extract_top_keywords(job_desc, top_n=20)
        jd_skills     = svc.extract_skills(job_desc)
        jd_word_count = svc.word_count(job_desc)

    # ── Process each resume ────────────────────────────────────────────────────
    results = []
    for file in files:
        entry = svc.process_resume(file, job_desc, jd_keywords, jd_skills)
        if entry:
            # Prefer manually entered experience over auto-detected
            if candidate_info["exp_years"] > 0:
                entry["experience_years"] = candidate_info["exp_years"]
            entry["candidate_info"] = candidate_info
            results.append(entry)

    results.sort(key=lambda x: x["score"], reverse=True)
    resume_count = len(results)

    # ── Interview track & company match ───────────────────────────────────────
    interview_track = matched_companies = None
    if results or candidate_info["exp_years"] > 0:
        exp = candidate_info["exp_years"] or (results[0]["experience_years"] if results else 0)
        interview_track = svc.get_interview_track(exp)

        all_skills = list(dict.fromkeys(s for r in results for s in r.get("resume_skills", [])))
        matched_companies = svc.match_companies(
            all_skills, exp,
            candidate_info["target_role"],
            candidate_info["preferred_company_type"],
        )

    # ── Persist to DB ──────────────────────────────────────────────────────────
    session = None
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

    # ── Build detected skills for autofill ────────────────────────────────────
    unique_skills = list(dict.fromkeys(s for r in results for s in r.get("resume_skills", [])))[:10]

    ctx.update({
        'results': results,
        'jd_keywords': jd_keywords,
        'jd_skills': jd_skills,
        'jd_word_count': jd_word_count,
        'resume_count': resume_count,
        'session': session,
        'interview_track': interview_track,
        'matched_companies': matched_companies or [],
        'candidate_info': candidate_info,
        'detected_skills_json': json.dumps(unique_skills),
        'chart_labels_json': json.dumps([r["name"][:20] for r in results]),
        'chart_scores_json': json.dumps([r["score"] for r in results]),
        'chart_ats_json':    json.dumps([r["ats_score"] for r in results]),
    })
    return render(request, 'resume_screener/screener.html', ctx)


# ── History ────────────────────────────────────────────────────────────────────

def screener_history(request):
    sessions = ScreeningSession.objects.prefetch_related('results').all()
    return render(request, 'resume_screener/screener_history.html', {'sessions': sessions})


@require_http_methods(['POST'])
def delete_session(request, pk):
    session = get_object_or_404(ScreeningSession, pk=pk)
    session.delete()
    return redirect('screener_history')


# ── Shared session (read-only view) ───────────────────────────────────────────

def shared_session(request, token):
    session = get_object_or_404(ScreeningSession, share_token=token)
    results = [
        {
            "name": r.filename, "score": r.score,
            "strength": {"label": r.strength_label, "color": r.strength_color, "emoji": r.strength_emoji, "tier": r.strength_tier},
            "resume_skills": r.resume_skills,
            "matched_keywords": r.matched_keywords, "missing_keywords": r.missing_keywords,
            "matched_skills": r.matched_skills,   "missing_skills": r.missing_skills,
            "kw_score": r.kw_score, "skill_score": r.skill_score,
            "word_count": r.word_count, "ats_score": r.ats_score, "ats_details": r.ats_details,
        }
        for r in session.results.all()
    ]
    return render(request, 'resume_screener/screener.html', {
        'results': results,
        'jd_keywords': svc.extract_top_keywords(session.job_description, top_n=12),
        'jd_skills':   svc.extract_skills(session.job_description),
        'jd_word_count': session.jd_word_count,
        'resume_count':  session.resume_count,
        'session': session,
        'is_shared_view': True,
        'detected_skills_json': '[]',
        'interview_track': None,
        'matched_companies': [],
        'candidate_info': {},
        'chart_labels_json': json.dumps([r["name"][:20] for r in results]),
        'chart_scores_json': json.dumps([r["score"] for r in results]),
        'chart_ats_json':    json.dumps([r["ats_score"] for r in results]),
    })


# ── PDF report download ────────────────────────────────────────────────────────

def download_report(request, token):
    session = get_object_or_404(ScreeningSession, share_token=token)
    results = session.results.order_by('rank')

    try:
        import fitz as _fitz

        doc  = _fitz.open()
        M    = 50
        PW, PH = 595, 842

        C_BRAND   = (0.318, 0.42, 0.925)
        C_EMERALD = (0.204, 0.831, 0.6)
        C_AMBER   = (0.98, 0.749, 0.141)
        C_ROSE    = (0.984, 0.443, 0.522)
        C_CYAN    = (0.133, 0.827, 0.933)
        C_DARK    = (0.059, 0.078, 0.118)
        C_MID     = (0.58, 0.639, 0.722)
        C_LIGHT   = (0.945, 0.961, 0.988)
        C_WHITE   = (1, 1, 1)

        def new_page():
            p = doc.new_page(width=PW, height=PH)
            p.draw_rect(_fitz.Rect(0, 0, PW, PH), color=None, fill=C_DARK)
            return p

        def sc(tier):
            return {"A": C_EMERALD, "B": C_CYAN, "C": C_AMBER, "D": C_ROSE}.get(tier, C_MID)

        # Cover page
        page = new_page()
        page.draw_rect(_fitz.Rect(0, 0, PW, 120), color=None, fill=(0.07, 0.09, 0.22))
        page.draw_line(_fitz.Point(0, 120), _fitz.Point(PW, 120), color=C_BRAND, width=2)
        page.insert_text((M, 52), "CareerCompass", fontsize=22, color=C_WHITE, fontname="helv")
        page.insert_text((M, 80), "Resume Screening Report", fontsize=13, color=C_MID, fontname="helv")

        y = 148
        jd_preview = (session.job_description[:200] + "...") if len(session.job_description) > 200 else session.job_description
        page.insert_text((M, y), "Job Description (preview):", fontsize=9, color=C_MID, fontname="helv")
        y += 18
        words, line, lines = jd_preview.split(), [], []
        for w in words:
            line.append(w)
            if len(" ".join(line)) > 85:
                lines.append(" ".join(line[:-1])); line = [w]
        if line: lines.append(" ".join(line))
        for l in lines[:6]:
            page.insert_text((M, y), l, fontsize=9, color=C_LIGHT, fontname="helv"); y += 14

        y += 12
        for label, val in [
            ("Resumes Screened", str(session.resume_count)),
            ("Screening Date", session.created_at.strftime("%d %b %Y, %I:%M %p")),
            ("Top Score", f"{results.first().score:.1f}%" if results.exists() else "—"),
        ]:
            page.insert_text((M, y), f"{label}:", fontsize=9, color=C_MID, fontname="helv")
            page.insert_text((220, y), val, fontsize=9, color=C_WHITE, fontname="helv"); y += 18

        y += 20
        page.draw_line(_fitz.Point(M, y), _fitz.Point(PW - M, y), color=C_BRAND, width=0.5); y += 14
        page.insert_text((M, y), "Ranked Results", fontsize=13, color=C_WHITE, fontname="helv"); y += 22

        cols = [M, 80, 240, 330, 420, 480]
        for i, h in enumerate(["#", "Filename", "Match", "Grade", "ATS", "Keywords"]):
            page.insert_text((cols[i], y), h, fontsize=8, color=C_MID, fontname="helv")
        y += 4
        page.draw_line(_fitz.Point(M, y + 4), _fitz.Point(PW - M, y + 4), color=(0.2, 0.23, 0.38), width=0.5); y += 14

        for r in results:
            if y > PH - 80:
                page = new_page(); y = 80
            color = sc(r.strength_tier)
            total_kw = len(r.matched_keywords) + len(r.missing_keywords)
            for i, val in enumerate([str(r.rank), r.filename[:28], f"{r.score:.1f}%", r.strength_tier, f"{r.ats_score}%", f"{len(r.matched_keywords)}/{total_kw}"]):
                page.insert_text((cols[i], y), val, fontsize=8, color=(color if i in (2, 3) else C_LIGHT), fontname="helv")
            y += 16

        # Per-resume detail pages
        for r in results:
            page = new_page()
            page.draw_rect(_fitz.Rect(0, 0, PW, 90), color=None, fill=(0.07, 0.09, 0.22))
            color = sc(r.strength_tier)
            page.draw_line(_fitz.Point(0, 90), _fitz.Point(PW, 90), color=color, width=2)
            page.insert_text((M, 34), f"#{r.rank}  {r.filename}", fontsize=14, color=C_WHITE, fontname="helv")
            page.insert_text((M, 58), f"{r.strength_emoji}  {r.strength_label}", fontsize=10, color=color, fontname="helv")
            page.insert_text((PW - 110, 38), f"{r.score:.1f}%", fontsize=22, color=color, fontname="helv")
            page.insert_text((PW - 110, 62), "Similarity", fontsize=8, color=C_MID, fontname="helv")

            y = 116
            def section(title):
                nonlocal y
                page.insert_text((M, y), title, fontsize=9, color=C_MID, fontname="helv")
                y += 4
                page.draw_line(_fitz.Point(M, y + 4), _fitz.Point(PW - M, y + 4), color=(0.2, 0.23, 0.38), width=0.4)
                y += 16

            section("Score Breakdown")
            for label, val, clr in [
                ("Similarity", r.score, C_BRAND), ("ATS Score", r.ats_score, C_EMERALD),
                ("Keyword Coverage", r.kw_score, C_CYAN), ("Skill Match", r.skill_score, C_AMBER),
            ]:
                page.insert_text((M, y), label + ":", fontsize=8, color=C_MID, fontname="helv")
                page.insert_text((200, y), f"{val:.0f}%", fontsize=8, color=C_WHITE, fontname="helv")
                fill_w = max(4, int(340 * min(val, 100) / 100))
                page.draw_rect(_fitz.Rect(M, y + 4, M + 340, y + 10), color=None, fill=(0.2, 0.23, 0.38))
                page.draw_rect(_fitz.Rect(M, y + 4, M + fill_w, y + 10), color=None, fill=clr)
                y += 22

            y += 6
            section("Matched Skills")
            page.insert_text((M, y), "  ".join(r.matched_skills[:12]) or "None", fontsize=8, color=C_EMERALD, fontname="helv"); y += 18
            section("Missing Skills")
            page.insert_text((M, y), "  ".join(r.missing_skills[:12]) or "None", fontsize=8, color=C_ROSE, fontname="helv"); y += 18

            page.draw_line(_fitz.Point(M, PH - 40), _fitz.Point(PW - M, PH - 40), color=(0.2, 0.23, 0.38), width=0.4)
            page.insert_text((M, PH - 24), "Generated by CareerCompass — AI-Powered Career Guidance", fontsize=7, color=C_MID, fontname="helv")

        pdf_bytes = doc.tobytes()
        resp = HttpResponse(pdf_bytes, content_type='application/pdf')
        resp['Content-Disposition'] = f'attachment; filename="screening_report_{session.share_token}.pdf"'
        return resp

    except Exception as e:
        return HttpResponse(f"PDF generation failed: {e}", status=500)


# ── API: extract skills from uploaded resume ───────────────────────────────────

def api_extract_skills(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    files = request.FILES.getlist("resume")
    if not files:
        return JsonResponse({"error": "No file uploaded"}, status=400)

    entry = svc.process_resume(files[0], "", [], [])
    if not entry:
        return JsonResponse({"error": "Invalid filename"}, status=400)

    from careers.career_engine import SKILLS_LIST as CAREER_SKILLS
    career_skill_lower = {s.lower(): s for s in CAREER_SKILLS}
    matched_career = [career_skill_lower[s.lower()] for s in entry["resume_skills"] if s.lower() in career_skill_lower]

    return JsonResponse({
        "all_detected": entry["resume_skills"],
        "career_skills": matched_career,
    })
