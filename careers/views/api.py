import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from ..career_engine import recommend, CAREER_PROFILES


@csrf_exempt
@require_http_methods(['POST'])
def api_recommend(request):
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    student = {
        'name': body.get('name', 'Student'),
        'branch': body.get('branch', ''),
        'cgpa': float(body.get('cgpa', 7.0)),
        'leetcode': int(body.get('leetcode', 0)),
        'github': int(body.get('github', 0)),
        'skills': body.get('skills', []),
    }
    results = recommend(student)
    api_results = [
        {
            'career': r['career'],
            'score': r['score'],
            'skills_have': r['skills_have'],
            'skills_missing': r['skills_missing'],
            'avg_salary': r['avg_salary'],
            'demand_trend': r['demand_trend'],
        }
        for r in results
    ]
    return JsonResponse(api_results, safe=False)


def api_careers(request):
    data = [
        {
            'name': name,
            'required_skills': p['required_skills'],
            'avg_salary': p['avg_salary'],
            'demand_trend': p['demand_trend'],
        }
        for name, p in CAREER_PROFILES.items()
    ]
    return JsonResponse(data, safe=False)
