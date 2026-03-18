import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_POST

from .forms import StudentProfileForm
from .models import StudentProfile, CareerRecommendation
from .career_matcher import recommend, ALL_SKILLS, CAREER_PROFILES


def home(request):
    return render(request, 'careers/home.html')


def profile_form(request):
    demo_data = None
    if request.GET.get('demo'):
        demo_data = {
            'name':     'Arjun Verma',
            'branch':   'Computer Science Engineering',
            'cgpa':     '8.2',
            'year':     '3rd Year',
            'leetcode': '120',
            'github':   '6',
            'skills':   ['Python', 'JavaScript', 'React', 'Git', 'SQL', 'DSA', 'HTML/CSS', 'Node.js'],
        }

    form = StudentProfileForm(initial=demo_data) if demo_data else StudentProfileForm()
    return render(request, 'careers/form.html', {
        'form':        form,
        'all_skills':  ALL_SKILLS,
        'demo_skills': json.dumps(demo_data['skills']) if demo_data else '[]',
    })


def analyze(request):
    if request.method != 'POST':
        return redirect('profile_form')

    form = StudentProfileForm(request.POST)
    if not form.is_valid():
        return render(request, 'careers/form.html', {
            'form':       form,
            'all_skills': ALL_SKILLS,
            'demo_skills':'[]',
            'errors':     form.errors,
        })

    data = form.cleaned_data

    profile = StudentProfile.objects.create(
        name     = data['name'],
        branch   = data['branch'],
        cgpa     = data['cgpa'],
        year     = data['year'],
        leetcode = data['leetcode'],
        github   = data['github'],
        skills   = data['skills'],
    )

    student_dict = {
        'name':     data['name'],
        'branch':   data['branch'],
        'cgpa':     data['cgpa'],
        'leetcode': data['leetcode'],
        'github':   data['github'],
        'skills':   data['skills'],
    }
    recommendations = recommend(student_dict)

    for rank, rec in enumerate(recommendations, 1):
        CareerRecommendation.objects.create(
            student        = profile,
            career         = rec['career'],
            score          = rec['score'],
            skills_have    = rec['skills_have'],
            skills_missing = rec['skills_missing'],
            avg_salary     = rec['avg_salary'],
            demand_trend   = rec['demand_trend'],
            rank           = rank,
        )

    top = recommendations[0]

    return render(request, 'careers/results.html', {
        'profile':         profile,
        'recommendations': recommendations,
        'top':             top,
        'all_skills_json': json.dumps(data['skills']),
        'results_json':    json.dumps([
            {'career': r['career'], 'score': r['score']} for r in recommendations
        ]),
    })


def careers_list(request):
    return render(request, 'careers/careers_list.html', {'careers': CAREER_PROFILES})


def history(request):
    # Removed the :20 cap — pagination is now handled in the template JS
    profiles = StudentProfile.objects.prefetch_related('recommendations').order_by('-created_at')
    return render(request, 'careers/history.html', {'profiles': profiles})


def skill_roadmap(request):
    return render(request, 'careers/skill_roadmap.html')


@require_POST
def delete_profile(request, profile_id):
    """Delete a StudentProfile (and its recommendations via CASCADE) via AJAX."""
    try:
        profile = get_object_or_404(StudentProfile, id=profile_id)
        profile.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(['POST'])
def api_recommend(request):
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    student = {
        'name':     body.get('name', 'Student'),
        'branch':   body.get('branch', ''),
        'cgpa':     float(body.get('cgpa', 7.0)),
        'leetcode': int(body.get('leetcode', 0)),
        'github':   int(body.get('github', 0)),
        'skills':   body.get('skills', []),
    }
    results = recommend(student)
    api_results = [
        {
            'career':         r['career'],
            'score':          r['score'],
            'skills_have':    r['skills_have'],
            'skills_missing': r['skills_missing'],
            'avg_salary':     r['avg_salary'],
            'demand_trend':   r['demand_trend'],
        }
        for r in results
    ]
    return JsonResponse(api_results, safe=False)


def api_careers(request):
    data = [
        {
            'name':            name,
            'required_skills': p['required_skills'],
            'avg_salary':      p['avg_salary'],
            'demand_trend':    p['demand_trend'],
        }
        for name, p in CAREER_PROFILES.items()
    ]
    return JsonResponse(data, safe=False)
