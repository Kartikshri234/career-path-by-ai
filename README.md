# 🎯 CareerCompass — Django Edition

An upgraded version of the AI Career Path Recommendation System built with **Django + SQLite**.

---

## 🚀 Quick Start

```bash
# 1. Navigate into the project
cd career-path-django

# 2. Create & activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run database migrations
python manage.py migrate

# 5. (Optional) Create admin superuser
python manage.py createsuperuser

# 6. Start the dev server
python manage.py runserver
```

Then open **http://127.0.0.1:8000** in your browser.

---

## 📁 Project Structure

```
career-path-django/
├── careercompass/              ← Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── careers/                    ← Main app
│   ├── career_engine.py        ← Upgraded scoring engine (5 careers)
│   ├── models.py               ← StudentProfile + AnalysisResult (saved to DB)
│   ├── views.py                ← Home, Analyze, Results, History, API
│   ├── forms.py                ← Django form with validation
│   ├── urls.py                 ← All URL routes
│   ├── admin.py                ← Django admin config
│   ├── templates/careers/
│   │   ├── base.html           ← Shared nav + layout
│   │   ├── home.html           ← Landing page
│   │   ├── form.html           ← Student profile form
│   │   ├── results.html        ← Career analysis results
│   │   └── history.html        ← All past analyses (NEW)
│   └── static/careers/css/
│       └── style.css           ← All styling
├── manage.py
└── requirements.txt
```

---

## 🌐 URL Routes

| URL                   | View       | Description                        |
|-----------------------|------------|------------------------------------|
| `/`                   | home       | Landing page                       |
| `/analyze/`           | analyze    | Profile form (GET) + submit (POST) |
| `/analyze/?demo=1`    | analyze    | Pre-filled demo profile            |
| `/results/<id>/`      | results    | Career analysis results page       |
| `/history/`           | history    | All saved analyses (NEW)           |
| `/admin/`             | Django admin | Manage profiles & results        |
| `/api/recommend/`     | api_recommend | POST JSON → ranked results      |
| `/api/careers/`       | api_careers   | GET all career tracks           |

---

## ✨ Upgrades over original

| Feature             | Original (HTML/FastAPI) | Django version         |
|---------------------|-------------------------|------------------------|
| Backend             | FastAPI / Static HTML   | Django 4.x             |
| Database            | None                    | SQLite (auto-saved)    |
| Form validation     | JS only                 | Django Forms + CSRF    |
| History             | ❌                      | ✅ `/history/` page    |
| Admin panel         | ❌                      | ✅ `/admin/`           |
| Career tracks       | 4                       | 5 (PM added)           |
| Demo mode           | JS button               | `?demo=1` URL param    |
| API                 | FastAPI `/docs`         | `/api/recommend/`      |

---

## 🧠 Scoring Formula

```
Match Score = (Skill Overlap × 60%) + (CGPA × 20%) + (LeetCode × 10%) + (GitHub × 10%)
Score range: 18–98 (floor boost so no student gets 0)
```
