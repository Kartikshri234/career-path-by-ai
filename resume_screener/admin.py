from django.contrib import admin
from .models import ScreeningSession, ResumeResult


class ResumeResultInline(admin.TabularInline):
    model = ResumeResult
    extra = 0
    readonly_fields = ('filename', 'score', 'strength_label', 'ats_score', 'rank')
    fields = ('rank', 'filename', 'score', 'strength_label', 'ats_score')


@admin.register(ScreeningSession)
class ScreeningSessionAdmin(admin.ModelAdmin):
    list_display  = ('id', 'short_jd', 'resume_count', 'created_at', 'share_token')
    list_filter   = ('created_at',)
    search_fields = ('job_description',)
    readonly_fields = ('share_token', 'created_at')
    inlines       = [ResumeResultInline]

    def short_jd(self, obj):
        return obj.job_description[:60] + "…"
    short_jd.short_description = "Job Description"


@admin.register(ResumeResult)
class ResumeResultAdmin(admin.ModelAdmin):
    list_display  = ('filename', 'score', 'ats_score', 'strength_tier', 'rank', 'session')
    list_filter   = ('strength_tier',)
    search_fields = ('filename',)
