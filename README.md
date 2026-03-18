# 🎯 CareerCompass — Django Edition

An AI-powered career path recommendation system for engineering students.
Enter your profile — CGPA, LeetCode count, GitHub repos, and skills — and get
instant career match scores, skill gap analysis, city-wise salary data, a
personalised 12-week roadmap, and much more.

Built with **Django 4.x · SQLite · Chart.js · Vanilla JS · CSS Design System**.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🎯 Career Matching | Weighted scoring across 5 career tracks |
| 🔍 Skill Gap Analysis | See exactly which skills you have vs need |
| 🗺️ 12-Week Roadmap | Week-by-week plan with curated resources |
| 📊 Radar Chart | Your skills vs required — visual comparison |
| 💰 Salary Insights | City-wise salary data (India + Remote) |
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

# 4. Apply database migrations
python manage.py migrate

# 5. (Optional) Create an admin superuser
python manage.py createsuperuser

# 6. Run the development server
python manage.py runserver
```

Then open **http://127.0.0.1:8000** in your browser.

---

## 📁 Project Structure

```
careercompass/
├── manage.py
├── requirements.txt
├── README.md
├── db.sqlite3                          ← Auto-created SQLite database
│
├── careercompass/                      ← Django project config
│   ├── settings.py                     ← App settings (timezone: Asia/Kolkata)
│   ├── urls.py                         ← Root URL config
│   └── wsgi.py
│
└── careers/                            ← Main Django app
    ├── career_engine.py                ← Full scoring engine + career data
    ├── career_matcher.py               ← Legacy scoring module (still used)
    ├── models.py                       ← StudentProfile + CareerRecommendation
    ├── views.py                        ← All page + API views + delete endpoint
    ├── forms.py                        ← StudentProfileForm with validation
    ├── urls.py                         ← All URL routes
    ├── admin.py                        ← Admin with list_display, search, filters
    ├── migrations/
    │   └── 0001_initial.py
    ├── static/careers/
    │   ├── css/style.css               ← Full design system (dark + light theme)
    │   └── js/main.js                  ← Scroll reveal, 3D tilt, count-up, tabs
    └── templates/careers/
        ├── base.html                   ← Shared nav, fonts, Chart.js, theme toggle
        ├── home.html                   ← Landing page with hero + feature cards
        ├── form.html                   ← Student profile input form
        ├── results.html                ← Career results with tabs + radar chart
        ├── careers_list.html           ← Expandable career cards with 6 tabs each
        ├── history.html                ← Searchable, filterable, paginated history
        └── skill_roadmap.html          ← 3-step interactive skill planner
```

---

## 🌐 URL Routes

| URL | View | Description |
|---|---|---|
| `/` | `home` | Landing page |
| `/profile/` | `profile_form` | Student profile form |
| `/profile/?demo=1` | `profile_form` | Pre-filled demo profile |
| `/analyze/` | `analyze` | POST — runs scoring, saves to DB |
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
Score = (Skill Match × 60%) + (CGPA × 20%) + (LeetCode × 10%) + (GitHub × 10%)
```

Each career has custom weights. For example:
- **Cloud / DevOps** weights GitHub at 20% (projects matter more than CGPA)
- **Data Scientist** weights CGPA at 25% (academic foundation matters more)
- **Cybersecurity** weights Skill Match at 65% (very skill-specific field)

Scores are normalised to a range of **18–98** so no student ever gets 0.

---

## 🗂️ Career Tracks

| Career | Icon | Avg Salary | Demand |
|---|---|---|---|
| Software Development Engineer | 💻 | ₹8–35 LPA | Very High ↑ |
| Data Scientist / ML Engineer | 🤖 | ₹10–45 LPA | High ↑ |
| Cloud / DevOps Engineer | ☁️ | ₹9–40 LPA | High ↑ |
| Cybersecurity Engineer | 🔐 | ₹8–32 LPA | Growing ↑ |
| Product Manager (Tech) | 📋 | ₹12–50 LPA | Moderate → |

Each career includes: required skills, scoring weights, 5-phase 12-week roadmap,
city-wise salary data, job roles, top hiring companies, certifications, day-in-life
description, and a career growth path.

---

## 🗄️ Database Models

### `StudentProfile`
Stores every submitted profile automatically.

| Field | Type | Description |
|---|---|---|
| `name` | CharField | Student name |
| `branch` | CharField | Engineering branch |
| `cgpa` | FloatField | CGPA out of 10 |
| `year` | CharField | Year of study |
| `leetcode` | IntegerField | Problems solved |
| `github` | IntegerField | Public repositories |
| `skills` | JSONField | List of selected skills |
| `created_at` | DateTimeField | Auto timestamp |

### `CareerRecommendation`
Stores ranked results linked to each profile (FK → StudentProfile, CASCADE delete).

| Field | Type | Description |
|---|---|---|
| `career` | CharField | Career track name |
| `score` | IntegerField | Match score (18–98) |
| `rank` | IntegerField | Position in ranked results |
| `skills_have` | JSONField | Skills the student has |
| `skills_missing` | JSONField | Skills to learn |
| `avg_salary` | CharField | Salary range |
| `demand_trend` | CharField | Market demand |

---

## 🎨 Frontend Design

The frontend is a custom design system called **"Deep Cosmos × Neon Precision"** with:

- **Fonts:** Syne (headings) · DM Sans (body) · DM Mono (code) via Google Fonts
- **Dark/Light theme** with full CSS variable token system
- **Micro-animations:** scroll reveal, 3D card tilt, count-up, progress bars, button glow
- **Glassmorphism** floating navbar with `backdrop-filter: blur`
- **Chart.js** radar charts on results and careers pages
- **Starfield background** in dark mode via CSS radial gradients

---

## ⚙️ Configuration

Key settings in `careercompass/settings.py`:

```python
DEBUG = True                        # Set False in production
TIME_ZONE = 'Asia/Kolkata'          # Change for your region
ALLOWED_HOSTS = ['*']               # Restrict in production

# Database — SQLite by default
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# To switch to PostgreSQL:
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'careercompass_db',
#         'USER': 'your_user',
#         'PASSWORD': 'your_password',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11 · Django 4.x |
| Database | SQLite (dev) · PostgreSQL-ready |
| Frontend | HTML · CSS (custom design system) · Vanilla JS |
| Charts | Chart.js 4.4 (CDN) |
| Fonts | Google Fonts (Syne, DM Sans, DM Mono) |
| Version Control | Git |

---

## 📋 What's Inside Each Page

### `/careers/` — Career Tracks Explorer
Each career card is clickable and expands to show **6 tabs**:
- **Overview** — salary, demand, difficulty, day-in-life, growth path, scoring weights
- **Roles** — job titles, top hiring companies, recommended certifications
- **Roadmap** — 5-phase 12-week learning plan with resources
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

## 🚧 Future Improvements

- [ ] User authentication (login / signup)
- [ ] PDF export of results
- [ ] Resume parser — auto-fill skills from uploaded PDF
- [ ] Progress tracker — mark roadmap tasks as done (persistent)
- [ ] Shareable result links
- [ ] Score history chart over multiple submissions
- [ ] More career tracks (UI/UX, Embedded, Blockchain)
- [ ] PWA support (installable on mobile)

---

## 👨‍💻 Author

Built by **Kartik** · CareerCompass Django Edition · 2025–2026
