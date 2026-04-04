from django.http import JsonResponse

from . import screener_service as svc


def api_extract_skills(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST only'}, status=405)

    files = request.FILES.getlist('resume')
    if not files:
        return JsonResponse({'error': 'No file uploaded'}, status=400)

    entry = svc.process_resume(files[0], '', [], [])
    if not entry:
        return JsonResponse({'error': 'Invalid filename'}, status=400)

    from careers.career_engine import SKILLS_LIST as CAREER_SKILLS
    career_skill_lower = {s.lower(): s for s in CAREER_SKILLS}
    matched_career = [career_skill_lower[s.lower()] for s in entry['resume_skills'] if s.lower() in career_skill_lower]

    return JsonResponse({
        'all_detected': entry['resume_skills'],
        'career_skills': matched_career,
    })
