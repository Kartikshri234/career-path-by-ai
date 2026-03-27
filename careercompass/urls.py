from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('careers.urls')),
    path('screener/', include('resume_screener.urls')),
]
