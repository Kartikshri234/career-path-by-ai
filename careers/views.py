import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
<<<<<<< HEAD
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .forms import StudentProfileForm
from .models import StudentProfile, CareerRecommendation
from .career_matcher import recommend, ALL_SKILLS, CAREER_PROFILES


def home(request):
    """Landing page."""
    return render(request, 'careers/home.html')


def profile_form(request):
    """Step 1 — fill in student profile."""
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
        'form': form,
        'all_skills': ALL_SKILLS,
        'demo_skills': json.dumps(demo_data['skills']) if demo_data else '[]',
    })


def analyze(request):
    """Step 2/3 — process form, run scoring, save to DB, show results."""
    if request.method != 'POST':
        return redirect('profile_form')

    form = StudentProfileForm(request.POST)
    if not form.is_valid():
        return render(request, 'careers/form.html', {
            'form': form,
            'all_skills': ALL_SKILLS,
            'demo_skills': '[]',
            'errors': form.errors,
        })

    data = form.cleaned_data

    # Save profile to DB
    profile = StudentProfile.objects.create(
        name     = data['name'],
        branch   = data['branch'],
        cgpa     = data['cgpa'],
        year     = data['year'],
        leetcode = data['leetcode'],
        github   = data['github'],
        skills   = data['skills'],
    )

    # Run scoring engine
    student_dict = {
        'name':     data['name'],
        'branch':   data['branch'],
        'cgpa':     data['cgpa'],
        'leetcode': data['leetcode'],
        'github':   data['github'],
        'skills':   data['skills'],
    }
    recommendations = recommend(student_dict)

    # Save recommendations to DB
    saved_recs = []
    for rank, rec in enumerate(recommendations, 1):
        saved = CareerRecommendation.objects.create(
            student        = profile,
            career         = rec['career'],
            score          = rec['score'],
            skills_have    = rec['skills_have'],
            skills_missing = rec['skills_missing'],
            avg_salary     = rec['avg_salary'],
            demand_trend   = rec['demand_trend'],
            rank           = rank,
        )
        saved_recs.append(rec)

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
    """API-style page listing all career tracks."""
    return render(request, 'careers/careers_list.html', {
        'careers': CAREER_PROFILES
    })


# ── REST API ENDPOINTS ─────────────────────────────────────────────────────────

def api_careers(request):
    """GET /api/careers/ — list all career tracks."""
    data = [
        {
            'name':             name,
            'required_skills':  p['required_skills'],
            'avg_salary':       p['avg_salary'],
            'demand_trend':     p['demand_trend'],
        }
        for name, p in CAREER_PROFILES.items()
    ]
    return JsonResponse(data, safe=False)


@csrf_exempt
@require_http_methods(['POST'])
def api_recommend(request):
    """POST /api/recommend/ — score a student profile.

    Body (JSON):
    {
        "name": "Arjun",
        "branch": "CSE",
        "cgpa": 8.2,
        "year": "3rd Year",
        "leetcode": 120,
        "github": 6,
        "skills": ["Python", "Git", "SQL"]
    }
    """
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    student = {
        'name':     body.get('name',     'Student'),
        'branch':   body.get('branch',   ''),
        'cgpa':     float(body.get('cgpa', 7.0)),
        'leetcode': int(body.get('leetcode', 0)),
        'github':   int(body.get('github', 0)),
        'skills':   body.get('skills', []),
    }

    results = recommend(student)
    # Strip non-serialisable roadmap/salary detail for API response
    api_results = [
        {
            'career':          r['career'],
            'score':           r['score'],
            'skills_have':     r['skills_have'],
            'skills_missing':  r['skills_missing'],
            'avg_salary':      r['avg_salary'],
            'demand_trend':    r['demand_trend'],
        }
        for r in results
    ]
    return JsonResponse(api_results, safe=False)


def history(request):
    """View past analyses stored in the DB."""
    profiles = StudentProfile.objects.prefetch_related('recommendations').order_by('-created_at')[:20]
    return render(request, 'careers/history.html', {'profiles': profiles})


def skill_roadmap(request):
    """Interactive skill roadmap planner."""
    return render(request, 'careers/skill_roadmap.html')
=======

from .forms import StudentProfileForm
from .models import StudentProfile, AnalysisResult
from .career_engine import recommend, SKILLS_LIST, CAREER_PROFILES


def home(request):
    return render(request, 'careers/home.html')


def analyze(request):
    if request.method == 'POST':
        form = StudentProfileForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            student = {
                'name':     d['name'],
                'branch':   d['branch'],
                'cgpa':     float(d['cgpa']),
                'year':     d['year'],
                'leetcode': int(d['leetcode']),
                'github':   int(d['github']),
                'skills':   list(d['skills']),
            }
            results = recommend(student)

            profile = StudentProfile.objects.create(
                name=student['name'],
                branch=student['branch'],
                cgpa=student['cgpa'],
                year=student['year'],
                leetcode=student['leetcode'],
                github=student['github'],
                skills=student['skills'],
            )
            analysis = AnalysisResult.objects.create(
                profile=profile,
                results_json=results,
                top_career=results[0]['career'],
                top_score=results[0]['score'],
            )
            return redirect('results', pk=analysis.pk)

        # Form invalid — re-render with errors
        selected = list(form.data.getlist('skills'))
        return render(request, 'careers/form.html', {
            'form': form,
            'skills': SKILLS_LIST,
            'selected_skills': selected,
        })

    # GET
    form = StudentProfileForm()
    return render(request, 'careers/form.html', {
        'form': form,
        'skills': SKILLS_LIST,
        'selected_skills': [],
    })


def results(request, pk):
    analysis = get_object_or_404(AnalysisResult, pk=pk)
    profile  = analysis.profile
    res_list = analysis.get_results()
    top      = res_list[0] if res_list else {}

    # Safely convert profile.skills to JSON string for the template
    skills_json = json.dumps(profile.skills if isinstance(profile.skills, list) else [])

    return render(request, 'careers/results.html', {
        'analysis':       analysis,
        'profile':        profile,
        'results':        res_list,
        'top':            top,
        'radar_labels':   json.dumps(top.get('radar_labels', [])),
        'radar_required': json.dumps(top.get('radar_required', [])),
        'profile_skills_json': skills_json,
    })


def history(request):
    analyses = AnalysisResult.objects.select_related('profile').all()[:50]
    return render(request, 'careers/history.html', {'analyses': analyses})


def api_recommend(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    try:
        data    = json.loads(request.body)
        results = recommend(data)
        return JsonResponse({'results': results})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def api_careers(request):
    careers = [
        {
            'name': n,
            'required_skills': p['required_skills'],
            'avg_salary': p['avg_salary'],
            'demand_trend': p['demand_trend'],
        }
        for n, p in CAREER_PROFILES.items()
    ]
    return JsonResponse({'careers': careers})
>>>>>>> 85979af9c9ab7ae4dc87a2ca7b9ae268d7bb6f8b
