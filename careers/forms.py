from django import forms
from .career_matcher import ALL_SKILLS


BRANCH_CHOICES = [
    ('', 'Select Branch'),
    ('Computer Science Engineering', 'Computer Science Engineering'),
    ('Information Technology',       'Information Technology'),
    ('Electronics & Communication',  'Electronics & Communication'),
    ('Electrical Engineering',       'Electrical Engineering'),
    ('Mechanical Engineering',       'Mechanical Engineering'),
    ('Data Science',                 'Data Science'),
]

YEAR_CHOICES = [
    ('', 'Select Year'),
    ('1st Year',  '1st Year'),
    ('2nd Year',  '2nd Year'),
    ('3rd Year',  '3rd Year'),
    ('4th Year',  '4th Year'),
    ('Graduated', 'Graduated'),
]

WORK_PREF_CHOICES = [
    ('', 'Select'),
    ('Building Products (SDE)', 'Building Products (SDE)'),
    ('Analyzing Data',          'Analyzing Data'),
    ('Security & Networks',     'Security & Networks'),
    ('Research & Innovation',   'Research & Innovation'),
    ('Consulting',              'Consulting'),
]

EXPERIENCE_CHOICES = [
    ('', 'Select'),
    ('No internships yet', 'No internships yet'),
    ('1 Internship',       '1 Internship'),
    ('2+ Internships',     '2+ Internships'),
    ('Freelance Projects', 'Freelance Projects'),
    ('Open Source',        'Open Source'),
]


class StudentProfileForm(forms.Form):
    name       = forms.CharField(
        max_length=100, required=False,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Rahul Sharma'})
    )
    branch     = forms.ChoiceField(choices=BRANCH_CHOICES, required=False)
    cgpa       = forms.FloatField(
        min_value=0, max_value=10, required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'e.g. 7.8', 'step': '0.1'})
    )
    year       = forms.ChoiceField(choices=YEAR_CHOICES, required=False)
    work_pref  = forms.ChoiceField(choices=WORK_PREF_CHOICES, required=False)
    experience = forms.ChoiceField(choices=EXPERIENCE_CHOICES, required=False)
    leetcode   = forms.IntegerField(
        min_value=0, required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'e.g. 150'})
    )
    github     = forms.IntegerField(
        min_value=0, required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'e.g. 8'})
    )
    skills     = forms.MultipleChoiceField(
        choices=[(s, s) for s in ALL_SKILLS],
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    def clean(self):
        cleaned = super().clean()
        cleaned['name']     = cleaned.get('name')     or 'Student'
        cleaned['cgpa']     = cleaned.get('cgpa')     or 7.0
        cleaned['leetcode'] = cleaned.get('leetcode') or 0
        cleaned['github']   = cleaned.get('github')   or 0
        cleaned['skills']   = cleaned.get('skills')   or []
        return cleaned
