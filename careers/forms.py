from django import forms
<<<<<<< HEAD
from .career_matcher import ALL_SKILLS


BRANCH_CHOICES = [
    ('', 'Select Branch'),
    ('Computer Science Engineering', 'Computer Science Engineering'),
    ('Information Technology', 'Information Technology'),
    ('Electronics & Communication', 'Electronics & Communication'),
    ('Electrical Engineering', 'Electrical Engineering'),
    ('Mechanical Engineering', 'Mechanical Engineering'),
    ('Data Science', 'Data Science'),
]

YEAR_CHOICES = [
    ('', 'Select Year'),
    ('1st Year', '1st Year'),
    ('2nd Year', '2nd Year'),
    ('3rd Year', '3rd Year'),
    ('4th Year', '4th Year'),
    ('Graduated', 'Graduated'),
]

WORK_PREF_CHOICES = [
    ('', 'Select'),
    ('Building Products (SDE)', 'Building Products (SDE)'),
    ('Analyzing Data', 'Analyzing Data'),
    ('Security & Networks', 'Security & Networks'),
    ('Research & Innovation', 'Research & Innovation'),
    ('Consulting', 'Consulting'),
]

EXPERIENCE_CHOICES = [
    ('', 'Select'),
    ('No internships yet', 'No internships yet'),
    ('1 Internship', '1 Internship'),
    ('2+ Internships', '2+ Internships'),
    ('Freelance Projects', 'Freelance Projects'),
    ('Open Source', 'Open Source'),
]


class StudentProfileForm(forms.Form):
    name       = forms.CharField(
        max_length=100, required=False,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Rahul Sharma', 'id': 'fn'})
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
        # Provide defaults for optional fields
        cleaned['name']     = cleaned.get('name') or 'Student'
        cleaned['cgpa']     = cleaned.get('cgpa') or 7.0
        cleaned['leetcode'] = cleaned.get('leetcode') or 0
        cleaned['github']   = cleaned.get('github') or 0
        cleaned['skills']   = cleaned.get('skills') or []
        return cleaned
=======
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
>>>>>>> 85979af9c9ab7ae4dc87a2ca7b9ae268d7bb6f8b
