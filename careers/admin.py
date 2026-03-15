from django.contrib import admin
from .models import StudentProfile, CareerRecommendation


class CareerRecommendationInline(admin.TabularInline):
    model = CareerRecommendation
    extra = 0
    readonly_fields = ('career', 'score', 'skills_have', 'skills_missing', 'avg_salary', 'demand_trend', 'rank')


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
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
