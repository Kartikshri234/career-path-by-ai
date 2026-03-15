from django.contrib import admin
<<<<<<< HEAD
from .models import StudentProfile, CareerRecommendation


class CareerRecommendationInline(admin.TabularInline):
    model = CareerRecommendation
    extra = 0
    readonly_fields = ('career', 'score', 'skills_have', 'skills_missing', 'avg_salary', 'demand_trend', 'rank')
=======
from .models import StudentProfile, AnalysisResult
>>>>>>> 85979af9c9ab7ae4dc87a2ca7b9ae268d7bb6f8b


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
<<<<<<< HEAD
    list_display   = ('name', 'branch', 'cgpa', 'year', 'leetcode', 'github', 'created_at')
    list_filter    = ('branch', 'year')
    search_fields  = ('name',)
    inlines        = [CareerRecommendationInline]
    readonly_fields = ('created_at',)


@admin.register(CareerRecommendation)
class CareerRecommendationAdmin(admin.ModelAdmin):
    list_display  = ('student', 'career', 'score', 'rank', 'demand_trend')
    list_filter   = ('career',)
    search_fields = ('student__name', 'career')
=======
    list_display  = ('name', 'branch', 'cgpa', 'year', 'leetcode', 'github', 'created_at')
    list_filter   = ('branch', 'year')
    search_fields = ('name',)
    readonly_fields = ('created_at',)


@admin.register(AnalysisResult)
class AnalysisResultAdmin(admin.ModelAdmin):
    list_display  = ('profile', 'top_career', 'top_score', 'created_at')
    list_filter   = ('top_career',)
    readonly_fields = ('created_at',)
>>>>>>> 85979af9c9ab7ae4dc87a2ca7b9ae268d7bb6f8b
