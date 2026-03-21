# 🎯 CareerCompass — Django Edition

An AI-powered career path recommendation system for engineering students.
Enter your profile — CGPA, LeetCode count, GitHub repos, and skills — and get
instant career match scores, skill gap analysis, city-wise salary data, a
personalised 12-week roadmap, shareable result links, and much more.

Built with **Python 3.11 · Django 4.x · SQLite · Chart.js · Vanilla JS · CSS Design System**.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🎯 Career Matching | Weighted scoring across 5 career tracks |
| 🔍 Skill Gap Analysis | See exactly which skills you have vs need |
| 📊 Score Breakdown | Per-component contribution (skills, CGPA, LeetCode, GitHub) |
| 🗺️ 12-Week Roadmap | Week-by-week plan with curated resources |
| 📈 Radar Chart | Your skills vs required — visual comparison |
| 💰 Salary Insights | City-wise salary data (India + Remote) |
| 🔗 Shareable Results | Unique UUID link per analysis — share with anyone |
| 📜 History Page | All past analyses saved, searchable, filterable |
| 🗑️ Delete History | AJAX delete with confirm modal + toast notification |
| 📄 Pagination | 8 per page with numbered navigation |
| 🗂️ Careers Explorer | Clickable cards with 6 tabs of detail per career |
| 🗺️ Skill Roadmap Planner | 3-step wizard — pick skills, set pace, get plan |
| 🌗 Dark / Light Theme | Toggle with localStorage persistence |
| ⚡ Demo Mode | `?demo=1` auto-fills the form for instant testing |
| 🔌 REST API | JSON endpoints for external integrations |
| 🛠️ Django Admin | Full admin panel with search, filters, inline recs |

---

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd careercompass

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env and set SECRET_KEY, DEBUG, etc.

# 5. Apply database migrations
python manage.py migrate

# 6. (Optional) Create an admin superuser
python manage.py createsuperuser

# 7. Run the development server
python manage.py runserver
```

Then open **http://127.0.0.1:8000** in your browser.

---

## ⚙️ Environment Variables

All sensitive config lives in a `.env` file (development) or real environment
variables (production). Copy `.env.example` to `.env` and fill in your values.

| Variable | Default | Description |
|---|---|---|
| `SECRET_KEY` | `django-insecure-...` | Django secret key — **change in production** |
| `DEBUG` | `True` | Set `False` in production |
| `ALLOWED_HOSTS` | `*` | Comma-separated allowed hostnames |
| `DB_ENGINE` | `sqlite3` | `sqlite3` or `postgresql` |
| `DB_NAME` | `careercompass_db` | PostgreSQL database name |
| `DB_USER` | `postgres` | PostgreSQL user |
| `DB_PASSWORD` | _(empty)_ | PostgreSQL password |
| `DB_HOST` | `localhost` | PostgreSQL host |
| `DB_PORT` | `5432` | PostgreSQL port |
| `LANGUAGE_CODE` | `en-us` | Django language code |
| `TIME_ZONE` | `Asia/Kolkata` | Django timezone |

Generate a secure secret key:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## 📁 Project Structure

```
careercompass/
├── manage.py
├── requirements.txt
├── README.md
├── .env.example                        ← Copy to .env and fill in values
├── db.sqlite3                          ← Auto-created SQLite database
│
├── careercompass/                      ← Django project config
│   ├── settings.py                     ← All settings loaded from .env via python-decouple
│   ├── urls.py                         ← Root URL config
│   └── wsgi.py
│
├── careers/                            ← Main Django app
│   ├── career_engine.py                ← Full scoring engine + rich career data
│   ├── career_matcher.py               ← Core scoring module (used by views)
│   ├── models.py                       ← StudentProfile + CareerRecommendation
│   ├── views.py                        ← All page + API views + delete + shared result
│   ├── forms.py                        ← StudentProfileForm with validation
│   ├── urls.py                         ← All URL routes
│   ├── admin.py                        ← Admin with list_display, search, filters
│   └── migrations/
│       ├── 0001_initial.py
│       └── 0002_studentprofile_share_token.py
│
├── static/
│   ├── css/
│   │   ├── style.css                   ← Full design system (dark + light theme)
│   │   ├── careers_list.css
│   │   ├── history.css
│   │   └── skill_roadmap.css
│   └── js/
│       ├── main.js                     ← Scroll reveal, 3D tilt, count-up, tabs
│       ├── results.js
│       ├── careers_list.js
│       ├── history.js
│       └── skill_roadmap.js
│
├── staticfiles/                        ← Collected static files (WhiteNoise / production)
│
└── templates/careers/
    ├── base.html                       ← Shared nav, fonts, Chart.js, theme toggle
    ├── home.html                       ← Landing page with hero + feature cards
    ├── form.html                       ← Student profile input form
    ├── results.html                    ← Career results with tabs + radar chart
    ├── shared_result.html              ← Public read-only shareable result page
    ├── careers_list.html               ← Expandable career cards with 6 tabs each
    ├── history.html                    ← Searchable, filterable, paginated history
    └── skill_roadmap.html              ← 3-step interactive skill planner
```

---

## 🌐 URL Routes

| URL | View | Description |
|---|---|---|
| `/` | `home` | Landing page |
| `/profile/` | `profile_form` | Student profile form |
| `/profile/?demo=1` | `profile_form` | Pre-filled demo profile |
| `/analyze/` | `analyze` | POST — runs scoring, saves to DB |
| `/results/<uuid:token>/` | `shared_result` | Public shareable result page |
| `/careers/` | `careers_list` | Explore all 5 career tracks |
| `/history/` | `history` | All saved analyses |
| `/skill-roadmap/` | `skill_roadmap` | Interactive skill roadmap planner |
| `/delete-profile/<id>/` | `delete_profile` | AJAX POST — delete a profile |
| `/admin/` | Django admin | Manage profiles and recommendations |
| `/api/careers/` | `api_careers` | GET — all career tracks as JSON |
| `/api/recommend/` | `api_recommend` | POST — score a student profile |

---

## 🔌 REST API

### POST `/api/recommend/`
Score a student profile and return ranked career recommendations.

```bash
curl -X POST http://127.0.0.1:8000/api/recommend/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Arjun Verma",
    "cgpa": 8.2,
    "leetcode": 120,
    "github": 6,
    "skills": ["Python", "Git", "SQL", "DSA", "React"]
  }'
```

**Response:**
```json
[
  {
    "career": "Software Development Engineer",
    "score": 76,
    "skills_have": ["Python", "Git", "SQL", "DSA"],
    "skills_missing": ["System Design", "Java", "REST APIs"],
    "avg_salary": "₹8–35 LPA",
    "demand_trend": "Very High ↑"
  },
  ...
]
```

### GET `/api/careers/`
Returns all 5 career tracks with required skills, salary, and demand data.

---

## 🧠 Scoring Formula

```
Score = base(18) + [Skill Match × weight_skill + CGPA × weight_cgpa + LeetCode × weight_lc + GitHub × weight_gh] × 80
```

Scores are normalised to a range of **18–98** so no student ever gets 0.

Each career has custom weights tuned to that field's hiring reality:

| Career | Skill | CGPA | LeetCode | GitHub |
|---|---|---|---|---|
| Software Development Engineer | 60% | 20% | 10% | 10% |
| Data Scientist / ML Engineer | 60% | 25% | 5% | 10% |
| Cloud / DevOps Engineer | 60% | 15% | 5% | 20% |
| Cybersecurity Engineer | 65% | 15% | 5% | 15% |
| Product Manager (Tech) | 50% | 20% | 10% | 20% |

The results page also shows a **score breakdown** — each component's exact
point contribution so students understand exactly what to improve.

---

## 🗂️ Career Tracks

| Career | Icon | Avg Salary | Demand | Difficulty |
|---|---|---|---|---|
| Software Development Engineer | 💻 | ₹8–35 LPA | Very High ↑ | Medium |
| Data Scientist / ML Engineer | 🤖 | ₹10–45 LPA | High ↑ | Hard |
| Cloud / DevOps Engineer | ☁️ | ₹9–40 LPA | High ↑ | Medium |
| Cybersecurity Engineer | 🔐 | ₹8–32 LPA | Growing ↑ | Hard |
| Product Manager (Tech) | 📋 | ₹12–50 LPA | Moderate → | Medium |

Each career includes: required skills, scoring weights, 5-phase 12-week roadmap,
city-wise salary data, job roles, top hiring companies, certifications, day-in-life
description, growth path, and a competency radar chart.

---

## 🗄️ Database Models

### `StudentProfile`
Stores every submitted profile automatically.

| Field | Type | Description |
|---|---|---|
| `name` | CharField | Student name |
| `branch` | CharField | Engineering branch (CSE, IT, ECE, EE, ME, DS) |
| `cgpa` | FloatField | CGPA out of 10 |
| `year` | CharField | Year of study |
| `leetcode` | IntegerField | Problems solved |
| `github` | IntegerField | Public repositories |
| `skills` | JSONField | List of selected skills |
| `share_token` | UUIDField | Auto-generated UUID for shareable links |
| `created_at` | DateTimeField | Auto timestamp |

### `CareerRecommendation`
Stores ranked results linked to each profile (FK → StudentProfile, CASCADE delete).

| Field | Type | Description |
|---|---|---|
| `student` | ForeignKey | Links to StudentProfile |
| `career` | CharField | Career track name |
| `score` | IntegerField | Match score (18–98) |
| `rank` | IntegerField | Position in ranked results |
| `skills_have` | JSONField | Skills the student has |
| `skills_missing` | JSONField | Skills to learn |
| `avg_salary` | CharField | Salary range |
| `demand_trend` | CharField | Market demand |

---

## 🔗 Shareable Results

Every analysis generates a unique UUID token stored on `StudentProfile.share_token`.
After analysing, a shareable URL is displayed:

```
http://127.0.0.1:8000/results/<uuid>/
```

Anyone with the link can view the full read-only results page — no login required.
This is served by the `shared_result` view using `shared_result.html`.

---

## 🎨 Frontend Design

The frontend is a custom design system called **"Deep Cosmos × Neon Precision"** with:

- **Fonts:** Syne (headings) · DM Sans (body) · DM Mono (code) via Google Fonts
- **Dark / Light theme** with full CSS variable token system
- **Micro-animations:** scroll reveal, 3D card tilt, count-up, progress bars, button glow
- **Glassmorphism** floating navbar with `backdrop-filter: blur`
- **Chart.js** radar charts on results and careers pages
- **Starfield background** in dark mode via CSS radial gradients

---

## 📋 What's Inside Each Page

### `/careers/` — Career Tracks Explorer
Each career card expands to show **6 tabs**:
- **Overview** — salary, demand, difficulty, day-in-life, growth path, scoring weights
- **Roles** — job titles, top hiring companies, recommended certifications
- **Roadmap** — 5-phase 12-week learning plan with curated resources
- **Salaries** — bar chart + city-wise salary cards
- **Skills** — all required skills with tips
- **Radar** — Chart.js radar showing required competency levels

Filter buttons: All · Very High Demand · High Demand · Top Salary · Medium Difficulty · Hard

### `/history/` — Analysis History
- Live search by name, branch, career, or skills
- Filter by career track (SDE / Data / Cloud / Cyber / PM)
- Sort by newest, oldest, highest score, or name A–Z
- Delete any entry with confirm modal + AJAX (no page reload)
- Pagination — 8 per page with numbered navigation

### `/skill-roadmap/` — Skill Roadmap Planner
A 3-step interactive wizard:
1. **Pick Skills** — animated tray with emoji chips, max 8 skills
2. **Timeline** — choose 4 / 8 / 12 / 16 weeks + beginner / intermediate / advanced
3. **Roadmap** — personalised week-by-week plan with tasks, resources, milestones, progress tracking

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11 · Django 4.x |
| Database | SQLite (dev) · PostgreSQL-ready |
| Frontend | HTML · CSS (custom design system) · Vanilla JS |
| Charts | Chart.js 4.4 (CDN) |
| Fonts | Google Fonts (Syne, DM Sans, DM Mono) |
| Static Files | WhiteNoise (production serving + compression) |
| Production Server | Gunicorn |
| Config Management | python-decouple (.env support) |
| Version Control | Git |

---

## 🚀 Production Deployment (Render)

1. Push your repo to GitHub.
2. Create a new **Web Service** on [Render](https://render.com).
3. Set **Build Command:** `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
4. Set **Start Command:** `gunicorn careercompass.wsgi`
5. Add environment variables in Render Dashboard → Environment:
   - `SECRET_KEY` — a strong random key
   - `DEBUG` — `False`
   - `ALLOWED_HOSTS` — `your-app.onrender.com`
   - `DB_ENGINE` — `sqlite3` (or `postgresql` with DB vars)

WhiteNoise handles static file serving automatically — no separate CDN needed for small deployments.

---

## 🚧 Future Improvements

- [ ] User authentication (login / signup)
- [ ] PDF export of results
- [ ] Resume parser — auto-fill skills from uploaded PDF
- [ ] Progress tracker — mark roadmap tasks as done (persistent)
- [ ] Score history chart over multiple submissions
- [ ] More career tracks (UI/UX, Embedded, Blockchain, Game Dev)
- [ ] PWA support (installable on mobile)
- [ ] Email notification with results summary

---

## 👨‍💻 Author

Built by **Kartik** · CareerCompass Django Edition · 2025–2026
