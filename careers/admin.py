from django.contrib import admin
from .models import StudentProfile, AnalysisResult


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display  = ('name', 'branch', 'cgpa', 'year', 'leetcode', 'github', 'created_at')
    list_filter   = ('branch', 'year')
    search_fields = ('name',)
    readonly_fields = ('created_at',)


@admin.register(AnalysisResult)
class AnalysisResultAdmin(admin.ModelAdmin):
    list_display  = ('profile', 'top_career', 'top_score', 'created_at')
    list_filter   = ('top_career',)
    readonly_fields = ('created_at',)
