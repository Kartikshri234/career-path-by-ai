from django.db import models


class CareerRecommendation(models.Model):
    student = models.ForeignKey('StudentProfile', on_delete=models.CASCADE, related_name='recommendations')
    career = models.CharField(max_length=100)
    score = models.IntegerField()
    skills_have = models.JSONField(default=list)
    skills_missing = models.JSONField(default=list)
    avg_salary = models.CharField(max_length=50)
    demand_trend = models.CharField(max_length=50)
    rank = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['rank']

    def __str__(self):
        return f"{self.student.name} → {self.career} ({self.score}%)"
