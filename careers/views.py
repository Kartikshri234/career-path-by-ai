import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse

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
