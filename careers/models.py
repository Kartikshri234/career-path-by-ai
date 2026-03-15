from django.db import models


class StudentProfile(models.Model):
    BRANCH_CHOICES = [
        ('CSE', 'Computer Science Engineering'),
        ('IT',  'Information Technology'),
        ('ECE', 'Electronics & Communication'),
        ('EE',  'Electrical Engineering'),
        ('ME',  'Mechanical Engineering'),
        ('DS',  'Data Science'),
    ]
    YEAR_CHOICES = [
        ('1', '1st Year'),
        ('2', '2nd Year'),
        ('3', '3rd Year'),
        ('4', '4th Year'),
        ('G', 'Graduated'),
    ]

    name      = models.CharField(max_length=100)
    branch    = models.CharField(max_length=50, choices=BRANCH_CHOICES)
    cgpa      = models.FloatField()
    year      = models.CharField(max_length=2, choices=YEAR_CHOICES)
    leetcode  = models.IntegerField(default=0)
    github    = models.IntegerField(default=0)
    skills    = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} — {self.branch} (CGPA: {self.cgpa})"


class CareerRecommendation(models.Model):
    student         = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='recommendations')
    career          = models.CharField(max_length=100)
    score           = models.IntegerField()
    skills_have     = models.JSONField(default=list)
    skills_missing  = models.JSONField(default=list)
    avg_salary      = models.CharField(max_length=50)
    demand_trend    = models.CharField(max_length=50)
    rank            = models.IntegerField(default=1)
    created_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['rank']

    def __str__(self):
        return f"{self.student.name} → {self.career} ({self.score}%)"
