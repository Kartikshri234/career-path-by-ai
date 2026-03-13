from django import forms
from .career_engine import SKILLS_LIST

BRANCH_CHOICES = [
    ('', 'Select your branch'),
    ('CSE',  'Computer Science Engineering'),
    ('IT',   'Information Technology'),
    ('ECE',  'Electronics & Communication'),
    ('EE',   'Electrical Engineering'),
    ('ME',   'Mechanical Engineering'),
    ('DS',   'Data Science'),
    ('Other','Other'),
]

YEAR_CHOICES = [
    ('', 'Select year'),
    ('1st', '1st Year'), ('2nd', '2nd Year'),
    ('3rd', '3rd Year'), ('4th', '4th Year'),
    ('grad','Graduated'),
]

INTEREST_CHOICES = [
    ('', 'Pick what sounds fun!'),
    ('sde',    'Building Products (SDE)'),
    ('data',   'Analysing Data'),
    ('sec',    'Security & Networks'),
    ('res',    'Research & Innovation'),
    ('consult','Consulting'),
]

EXP_CHOICES = [
    ('', 'Select'),
    ('none',   'No internships yet'),
    ('one',    '1 Internship'),
    ('multi',  '2+ Internships'),
    ('free',   'Freelance Projects'),
    ('oss',    'Open Source Contributor'),
]

SKILLS_CHOICES = [(s, s) for s in SKILLS_LIST]


class StudentProfileForm(forms.Form):
    name     = forms.CharField(max_length=120, required=False,
                   widget=forms.TextInput(attrs={'placeholder': 'e.g. Priya Sharma', 'id': 'fn'}))
    branch   = forms.ChoiceField(choices=BRANCH_CHOICES, required=False,
                   widget=forms.Select(attrs={'id': 'fb'}))
    cgpa     = forms.FloatField(min_value=0, max_value=10, required=False,
                   widget=forms.NumberInput(attrs={'placeholder': 'e.g. 7.8', 'step': '0.1', 'id': 'fg-cgpa'}))
    year     = forms.ChoiceField(choices=YEAR_CHOICES, required=False,
                   widget=forms.Select(attrs={'id': 'fy'}))
    interest = forms.ChoiceField(choices=INTEREST_CHOICES, required=False,
                   widget=forms.Select(attrs={'id': 'fw'}))
    experience = forms.ChoiceField(choices=EXP_CHOICES, required=False,
                   widget=forms.Select(attrs={'id': 'fe'}))
    leetcode = forms.IntegerField(min_value=0, required=False,
                   widget=forms.NumberInput(attrs={'placeholder': 'e.g. 120', 'id': 'flc'}))
    github   = forms.IntegerField(min_value=0, required=False,
                   widget=forms.NumberInput(attrs={'placeholder': 'e.g. 8', 'id': 'fgh'}))
    skills   = forms.MultipleChoiceField(choices=SKILLS_CHOICES, required=False,
                   widget=forms.CheckboxSelectMultiple())

    def clean_cgpa(self):
        val = self.cleaned_data.get('cgpa')
        return val if val is not None else 7.0

    def clean_leetcode(self):
        val = self.cleaned_data.get('leetcode')
        return val if val is not None else 0

    def clean_github(self):
        val = self.cleaned_data.get('github')
        return val if val is not None else 0

    def clean_name(self):
        return self.cleaned_data.get('name') or 'Student'
