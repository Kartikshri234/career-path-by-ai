from django.db import models
import json


class StudentProfile(models.Model):
    BRANCH_CHOICES = [
        ('CSE',  'Computer Science Engineering'),
        ('IT',   'Information Technology'),
        ('ECE',  'Electronics & Communication'),
        ('EE',   'Electrical Engineering'),
        ('ME',   'Mechanical Engineering'),
        ('DS',   'Data Science'),
        ('Other','Other'),
    ]
    YEAR_CHOICES = [
        ('1st', '1st Year'), ('2nd', '2nd Year'),
        ('3rd', '3rd Year'), ('4th', '4th Year'),
        ('grad','Graduated'),
    ]

    name     = models.CharField(max_length=120)
    branch   = models.CharField(max_length=10, choices=BRANCH_CHOICES, blank=True)
    cgpa     = models.FloatField(default=7.0)
    year     = models.CharField(max_length=10, choices=YEAR_CHOICES, blank=True)
    leetcode = models.IntegerField(default=0)
    github   = models.IntegerField(default=0)
    skills   = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.get_branch_display()})"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Student Profile'


class AnalysisResult(models.Model):
    profile    = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='results')
    results_json = models.JSONField(default=list)
    top_career = models.CharField(max_length=200)
    top_score  = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_results(self):
        return self.results_json

    def __str__(self):
        return f"{self.profile.name} → {self.top_career} ({self.top_score}%)"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Analysis Result'
