from django.urls import path
from . import views

urlpatterns = [
    path('',                              views.screener,         name='screener'),
    path('history/',                      views.screener_history, name='screener_history'),
    path('results/<uuid:token>/',         views.shared_session,   name='shared_session'),
    path('delete/<int:pk>/',              views.delete_session,   name='delete_session'),
    path('report/<uuid:token>/',          views.download_report,  name='download_report'),
    path('api/extract-skills/',           views.api_extract_skills, name='api_extract_skills'),
]
