# CareerCompass

CareerCompass is a Django project with two core modules:

- Career recommendation for students (profile analysis, ranked career matches, skill gaps, history, and share links)
- Resume screening (job-description matching, ATS scoring, session history, and PDF report export)

## Tech Stack

- Python 3.11+
- Django 4.x
- SQLite (default)
- scikit-learn (TF-IDF + cosine similarity)
- PyMuPDF + python-docx (resume text extraction)
- WhiteNoise + Gunicorn (production serving)

## Current Project Structure

```text
careercompass/
|- manage.py
|- README.md
|- requirements.txt
|- db.sqlite3
|- careercompass/
|  |- settings.py
|  |- urls.py
|  `- wsgi.py
|- careers/
|  |- admin.py
|  |- apps.py
|  |- forms.py
|  |- career_engine.py
|  |- career_matcher.py
|  |- urls.py
|  |- views/
|  |  |- __init__.py
|  |  |- core.py
|  |  `- api.py
|  |- models/
|  |  |- __init__.py
|  |  |- student_profile.py
|  |  `- career_recommendation.py
|  `- migrations/
|- resume_screener/
|  |- admin.py
|  |- apps.py
|  |- screener_service.py
|  |- urls.py
|  |- views/
|  |  |- __init__.py
|  |  |- pages.py
|  |  |- report.py
|  |  `- api.py
|  |- models/
|  |  |- __init__.py
|  |  |- screening_session.py
|  |  `- resume_result.py
|  |- uploads/
|  `- migrations/
|- templates/
|  |- careers/
|  `- resume_screener/
|- static/
`- staticfiles/
```

## Main Features

### Careers module

- Student profile form and analysis
- Career scoring and ranked recommendations
- Skill gap and recommendation insights
- Shareable result links (`/results/<uuid>/`)
- Analysis history + delete profile
- Career list and skill roadmap pages
- API endpoints for careers and recommendations

### Resume screener module

- Upload one or more resumes (PDF/DOCX)
- TF-IDF + cosine similarity scoring against job description
- ATS-style scoring and keyword/skill overlap
- Session history and shareable session links
- PDF report generation
- API endpoint for extracting detected skills

## URL Map

### Root routing

- `/admin/` -> Django admin
- `/` -> careers app routes
- `/screener/` -> resume_screener routes

### Careers routes

- `/` -> home
- `/profile/` -> profile form
- `/analyze/` -> run recommendation
- `/careers/` -> careers list
- `/history/` -> profile history
- `/skill-roadmap/` -> roadmap page
- `/delete-profile/<int:pk>/` -> delete profile
- `/results/<uuid:token>/` -> shared result
- `/api/careers/` -> careers API
- `/api/recommend/` -> recommendation API

### Resume screener routes (prefixed by `/screener/`)

- `/screener/` -> screener page
- `/screener/history/` -> screening history
- `/screener/results/<uuid:token>/` -> shared session
- `/screener/delete/<int:pk>/` -> delete session
- `/screener/report/<uuid:token>/` -> download PDF report
- `/screener/api/extract-skills/` -> skills extraction API

## Data Models

### Careers app

- `StudentProfile`
- `CareerRecommendation`

### Resume screener app

- `ScreeningSession`
- `ResumeResult`

## Setup (Local)

1. Clone and open the project folder.
2. Create and activate a virtual environment.
3. Install dependencies.
4. Apply migrations.
5. Run the development server.

```bash
git clone <your-repo-url>
cd careercompass
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open: `http://127.0.0.1:8000/`

## Environment Variables

Create a local `.env` file in the project root and keep it out of Git.

Required keys (as used in `careercompass/settings.py`):

- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- Database-related values (`DB_ENGINE`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`)
- `LANGUAGE_CODE`
- `TIME_ZONE`

Example local values:

```env
SECRET_KEY=django-insecure-change-me-before-going-to-production
DEBUG=False
ALLOWED_HOSTS=*

DB_ENGINE=sqlite3
DB_NAME=careercompass_db
DB_USER=postgres
DB_PASSWORD=your_password_here
DB_HOST=localhost
DB_PORT=5432

LANGUAGE_CODE=en-us
TIME_ZONE=Asia/Kolkata
```

## Production Notes

- `gunicorn` is included for production serving.
- `whitenoise` is used for static file serving.
- Run collectstatic before deployment:

```bash
python manage.py collectstatic --noinput
```

## Quick Validation

After changes, run:

```bash
python manage.py check
```
