import uuid
from django.db import models


class ScreeningSession(models.Model):
    """Persisted resume screening session."""
    share_token     = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    job_description = models.TextField()
    jd_word_count   = models.IntegerField(default=0)
    resume_count    = models.IntegerField(default=0)
    created_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        snippet = self.job_description[:60].replace('\n', ' ')
        return f"Session #{self.pk} — {snippet}…"


class ResumeResult(models.Model):
    """One uploaded resume inside a ScreeningSession."""
    session         = models.ForeignKey(ScreeningSession, on_delete=models.CASCADE, related_name='results')
    filename        = models.CharField(max_length=255)
    score           = models.FloatField()
    strength_label  = models.CharField(max_length=50)
    strength_color  = models.CharField(max_length=30)
    strength_emoji  = models.CharField(max_length=10)
    strength_tier   = models.CharField(max_length=5)
    resume_skills   = models.JSONField(default=list)
    matched_keywords = models.JSONField(default=list)
    missing_keywords = models.JSONField(default=list)
    matched_skills  = models.JSONField(default=list)
    missing_skills  = models.JSONField(default=list)
    kw_score        = models.IntegerField(default=0)
    skill_score     = models.IntegerField(default=0)
    word_count      = models.IntegerField(default=0)
    ats_score       = models.IntegerField(default=0)
    ats_details     = models.JSONField(default=dict)
    rank            = models.IntegerField(default=1)

    class Meta:
        ordering = ['rank']

    def __str__(self):
        return f"{self.filename} — {self.score}% (Session #{self.session_id})"
