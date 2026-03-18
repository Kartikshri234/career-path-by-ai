from django.contrib import admin
from .models import StudentProfile, CareerRecommendation


class CareerRecommendationInline(admin.TabularInline):
    model = CareerRecommendation
    extra = 0
    readonly_fields = ('career', 'score', 'rank', 'avg_salary', 'demand_trend', 'skills_have', 'skills_missing')
    can_delete = False


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display  = ('name', 'branch', 'cgpa', 'year', 'leetcode', 'github', 'skill_count', 'created_at')
    list_filter   = ('branch', 'year', 'created_at')
    search_fields = ('name', 'branch')
    ordering      = ('-created_at',)
    readonly_fields = ('created_at',)
    inlines       = [CareerRecommendationInline]

    def skill_count(self, obj):
        return len(obj.skills) if obj.skills else 0
    skill_count.short_description = 'Skills'


@admin.register(CareerRecommendation)
class CareerRecommendationAdmin(admin.ModelAdmin):
    list_display  = ('student', 'career', 'score', 'rank', 'avg_salary', 'demand_trend', 'created_at')
    list_filter   = ('career', 'rank', 'created_at')
    search_fields = ('student__name', 'career')
    ordering      = ('-score',)
    readonly_fields = ('created_at',)
