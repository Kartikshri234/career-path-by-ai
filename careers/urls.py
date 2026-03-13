from django.urls import path
from . import views

urlpatterns = [
    path('',              views.home,         name='home'),
    path('analyze/',      views.analyze,      name='analyze'),
    path('results/<int:pk>/', views.results,  name='results'),
    path('history/',      views.history,      name='history'),

    # JSON API
    path('api/recommend/', views.api_recommend, name='api_recommend'),
    path('api/careers/',   views.api_careers,   name='api_careers'),
]
