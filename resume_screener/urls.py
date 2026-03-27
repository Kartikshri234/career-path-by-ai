from django.urls import path
from . import views

urlpatterns = [
    path('', views.screener, name='screener'),
]
