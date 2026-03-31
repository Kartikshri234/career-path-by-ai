import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .forms import StudentProfileForm
from .models import StudentProfile, CareerRecommendation
from .career_engine import recommend, SKILLS_LIST as ALL_SKILLS, CAREER_PROFILES


def home(request):
    return render(request, 'careers/home.html')


def profile_form(request):
    demo_data = None
    autofill_skills = []

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

    # Feature 1: Resume auto-fill — accept skills from screener via URL param
    skills_param = request.GET.get('skills', '')
    if skills_param and not demo_data:
        try:
            raw = json.loads(skills_param)
            # Filter to only valid SKILLS_LIST entries
            autofill_skills = [s for s in raw if s in ALL_SKILLS]
        except (json.JSONDecodeError, TypeError):
            autofill_skills = []

    form = StudentProfileForm(initial=demo_data) if demo_data else StudentProfileForm()

    prefill_skills = demo_data['skills'] if demo_data else autofill_skills

    return render(request, 'careers/form.html', {
        'form':           form,
        'all_skills':     ALL_SKILLS,
        'demo_skills':    json.dumps(prefill_skills),
        'autofill_skills': autofill_skills,
        'is_autofill':    bool(autofill_skills),
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

    share_url = request.build_absolute_uri(
        f'/results/{profile.share_token}/'
    )

    return render(request, 'careers/results.html', {
        'profile':         profile,
        'recommendations': recommendations,
        'top':             top,
        'share_url':       share_url,
        'all_skills_json': json.dumps(data['skills']),
        'results_json':    json.dumps([
            {'career': r['career'], 'score': r['score']} for r in recommendations
        ]),
    })


def careers_list(request):
    return render(request, 'careers/careers_list.html', {'careers': CAREER_PROFILES})


def skill_roadmap(request):
    return render(request, 'careers/skill_roadmap.html')


def history(request):
    profiles = StudentProfile.objects.prefetch_related('recommendations').all()
    return render(request, 'careers/history.html', {'profiles': profiles})


def delete_profile(request, pk):
    profile = get_object_or_404(StudentProfile, pk=pk)
    if request.method == 'POST':
        profile.delete()
        return redirect('history')
    return redirect('history')


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


def shared_result(request, token):
    profile = get_object_or_404(StudentProfile, share_token=token)

    student_dict = {
        'name':     profile.name,
        'branch':   profile.branch,
        'cgpa':     profile.cgpa,
        'leetcode': profile.leetcode,
        'github':   profile.github,
        'skills':   profile.skills,
    }
    recommendations = recommend(student_dict)
    top = recommendations[0]

    share_url = request.build_absolute_uri(
        f'/results/{profile.share_token}/'
    )

    return render(request, 'careers/shared_result.html', {
        'profile':         profile,
        'recommendations': recommendations,
        'top':             top,
        'share_url':       share_url,
        'all_skills_json': json.dumps(profile.skills),
        'results_json':    json.dumps([
            {'career': r['career'], 'score': r['score']} for r in recommendations
        ]),
    })
