import uuid
from django.db import models


class ScreeningSession(models.Model):
    """Persisted resume screening session."""
    share_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    job_description = models.TextField()
    jd_word_count = models.IntegerField(default=0)
    resume_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        snippet = self.job_description[:60].replace('\n', ' ')
        return f"Session #{self.pk} — {snippet}…"
