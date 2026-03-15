# 🎯 CareerCompass — Django Edition

Converted from FastAPI + Vanilla JS → Full Django web application.

## 🗂 Project Structure

```
careercompass_django/
├── manage.py
├── requirements.txt
├── careercompass/          ← Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── careers/                ← Main Django app
    ├── models.py           ← StudentProfile, CareerRecommendation (SQLite DB)
    ├── views.py            ← All page + API views
    ├── forms.py            ← StudentProfileForm
    ├── urls.py             ← URL routing
    ├── admin.py            ← Django admin registration
    ├── career_matcher.py   ← Scoring engine (ported from original)
    ├── migrations/         ← DB migrations
    └── templates/careers/
        ├── base.html       ← Shared layout, nav, dark theme CSS
        ├── home.html       ← Landing page
        ├── form.html       ← Profile input form (Step 1)
        ├── results.html    ← Analysis results with tabs (Step 3)
        ├── careers_list.html ← All career tracks
        └── history.html    ← Past analyses from DB
```

## 🚀 Quick Start

```bash
# 1. Install Django
pip install -r requirements.txt

# 2. Apply database migrations
python manage.py migrate

# 3. Create an admin user (optional)
python manage.py createsuperuser

# 4. Run the development server
python manage.py runserver
```

Then open: http://127.0.0.1:8000/

## 🌐 Pages

| URL               | Description                              |
|-------------------|------------------------------------------|
| `/`               | Landing page                             |
| `/profile/`       | Student profile form (Step 1)            |
| `/profile/?demo=1`| Auto-fill demo data                      |
| `/analyze/`       | POST endpoint — runs scoring, saves to DB|
| `/careers/`       | Browse all 5 career tracks               |
| `/history/`       | Past analyses stored in SQLite           |
| `/admin/`         | Django admin panel                       |

## 🔌 REST API Endpoints

| Method | URL               | Description                    |
|--------|-------------------|--------------------------------|
| GET    | `/api/careers/`   | List all career tracks (JSON)  |
| POST   | `/api/recommend/` | Score a student profile (JSON) |

### Example API call
```bash
curl -X POST http://127.0.0.1:8000/api/recommend/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Arjun",
    "cgpa": 8.2,
    "leetcode": 120,
    "github": 6,
    "skills": ["Python", "Git", "SQL", "DSA"]
  }'
```

## 🧠 Scoring Formula

```
Match Score = (Skill Overlap × 60%) + (CGPA × 20%) + (LeetCode × 10%) + (GitHub × 10%)
Score displayed as 18–98 range (floor boost so no one gets 0)
```

## 🗄️ Database

Uses SQLite by default (`db.sqlite3`). Two models:
- **StudentProfile** — stores every submitted profile
- **CareerRecommendation** — stores ranked results per profile (FK → StudentProfile)

To use PostgreSQL, update `DATABASES` in `settings.py`.
