from django.urls import path
from . import views

urlpatterns = [
    path('',             views.home,         name='home'),
    path('profile/',     views.profile_form, name='profile_form'),
    path('analyze/',     views.analyze,      name='analyze'),
    path('careers/',     views.careers_list, name='careers_list'),
    path('history/',      views.history,       name='history'),
    path('skill-roadmap/', views.skill_roadmap, name='skill_roadmap'),

    # JSON API endpoints
    path('api/careers/',   views.api_careers,   name='api_careers'),
    path('api/recommend/', views.api_recommend, name='api_recommend'),
]
