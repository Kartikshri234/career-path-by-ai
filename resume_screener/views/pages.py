import json

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods

from ..models import ScreeningSession, ResumeResult
from . import screener_service as svc


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

    if request.method != 'POST':
        return render(request, 'resume_screener/screener.html', ctx)

    # Collect form data.
    job_desc = request.POST.get('job_description', '').strip()
    files = request.FILES.getlist('resumes')

    candidate_info = {
        'name': request.POST.get('candidate_name', '').strip(),
        'email': request.POST.get('candidate_email', '').strip(),
        'target_role': request.POST.get('target_role', '').strip(),
        'exp_years': int(request.POST.get('exp_years', '0') or 0),
        'preferred_company_type': request.POST.get('preferred_company_type', '').strip(),
    }

    # JD analysis.
    jd_keywords = jd_skills = []
    jd_word_count = 0
    if job_desc:
        jd_keywords = svc.extract_top_keywords(job_desc, top_n=20)
        jd_skills = svc.extract_skills(job_desc)
        jd_word_count = svc.word_count(job_desc)

    # Process each resume.
    results = []
    for file in files:
        entry = svc.process_resume(file, job_desc, jd_keywords, jd_skills)
        if entry:
            # Prefer manually entered experience over auto-detected.
            if candidate_info['exp_years'] > 0:
                entry['experience_years'] = candidate_info['exp_years']
            entry['candidate_info'] = candidate_info
            results.append(entry)

    results.sort(key=lambda x: x['score'], reverse=True)
    resume_count = len(results)

    # Interview track and company match.
    interview_track = matched_companies = None
    if results or candidate_info['exp_years'] > 0:
        exp = candidate_info['exp_years'] or (results[0]['experience_years'] if results else 0)
        interview_track = svc.get_interview_track(exp)

        all_skills = list(dict.fromkeys(s for r in results for s in r.get('resume_skills', [])))
        matched_companies = svc.match_companies(
            all_skills,
            exp,
            candidate_info['target_role'],
            candidate_info['preferred_company_type'],
        )

    # Persist to DB.
    session = None
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
                filename=r['name'],
                score=r['score'],
                strength_label=r['strength']['label'],
                strength_color=r['strength']['color'],
                strength_emoji=r['strength']['emoji'],
                strength_tier=r['strength']['tier'],
                resume_skills=r['resume_skills'],
                matched_keywords=r['matched_keywords'],
                missing_keywords=r['missing_keywords'],
                matched_skills=r['matched_skills'],
                missing_skills=r['missing_skills'],
                kw_score=r['kw_score'],
                skill_score=r['skill_score'],
                word_count=r['word_count'],
                ats_score=r['ats_score'],
                ats_details=r['ats_details'],
            )

    # Build detected skills for autofill.
    unique_skills = list(dict.fromkeys(s for r in results for s in r.get('resume_skills', [])))[:10]

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
        'chart_labels_json': json.dumps([r['name'][:20] for r in results]),
        'chart_scores_json': json.dumps([r['score'] for r in results]),
        'chart_ats_json': json.dumps([r['ats_score'] for r in results]),
    })
    return render(request, 'resume_screener/screener.html', ctx)


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
    results = [
        {
            'name': r.filename,
            'score': r.score,
            'strength': {
                'label': r.strength_label,
                'color': r.strength_color,
                'emoji': r.strength_emoji,
                'tier': r.strength_tier,
            },
            'resume_skills': r.resume_skills,
            'matched_keywords': r.matched_keywords,
            'missing_keywords': r.missing_keywords,
            'matched_skills': r.matched_skills,
            'missing_skills': r.missing_skills,
            'kw_score': r.kw_score,
            'skill_score': r.skill_score,
            'word_count': r.word_count,
            'ats_score': r.ats_score,
            'ats_details': r.ats_details,
        }
        for r in session.results.all()
    ]
    return render(request, 'resume_screener/screener.html', {
        'results': results,
        'jd_keywords': svc.extract_top_keywords(session.job_description, top_n=12),
        'jd_skills': svc.extract_skills(session.job_description),
        'jd_word_count': session.jd_word_count,
        'resume_count': session.resume_count,
        'session': session,
        'is_shared_view': True,
        'detected_skills_json': '[]',
        'interview_track': None,
        'matched_companies': [],
        'candidate_info': {},
        'chart_labels_json': json.dumps([r['name'][:20] for r in results]),
        'chart_scores_json': json.dumps([r['score'] for r in results]),
        'chart_ats_json': json.dumps([r['ats_score'] for r in results]),
    })
