# 🧭 CareerCompass — AI-Powered Career Guidance Platform

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.x-092E20?style=flat-square&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)
![Chart.js](https://img.shields.io/badge/Chart.js-4.4-FF6384?style=flat-square&logo=chartdotjs&logoColor=white)
![WhiteNoise](https://img.shields.io/badge/WhiteNoise-6.6-lightgrey?style=flat-square)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.4-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)

**An AI-powered career path recommendation and resume screening platform for engineering students.**

[Features](#-features) · [Quick Start](#-quick-start) · [Project Structure](#-project-structure) · [API Reference](#-rest-api) · [Deployment](#-production-deployment-render)

</div>

---

## 📖 Overview

CareerCompass helps engineering students discover the right career path through a smart scoring engine that evaluates their CGPA, LeetCode problem count, GitHub repositories, and technical skills against 5 industry career tracks.

It also includes a fully-featured **AI Resume Screener** that uses TF-IDF vectorization and cosine similarity to rank multiple resumes against a job description — with skill gap analysis, keyword overlap, and match-grade verdicts.

Built with **Python 3.11 · Django 4.x · SQLite · scikit-learn · PyMuPDF · Chart.js · Vanilla JS**.

---

## ✨ Features

### 🎯 Career Recommendation Engine
| Feature | Description |
|---|---|
| 🎯 Smart Career Matching | Weighted scoring across 5 career tracks based on your actual profile |
| 🔍 Skill Gap Analysis | See exactly which skills you have vs. what each career requires |
| 📊 Score Breakdown | Per-component contribution — skills, CGPA, LeetCode, GitHub |
| 🗺️ 12-Week Roadmap | Personalised week-by-week plan with curated learning resources |
| 📈 Radar Chart | Visual skill comparison — your level vs. career requirement |
| 💰 Salary Insights | City-wise salary data for India + Remote positions |
| 🔗 Shareable Results | Unique UUID link per analysis — share with mentors or friends |
| 📜 Analysis History | All past analyses saved, searchable, and filterable |
| 🗑️ Delete History | Confirm-modal delete with AJAX (no page reload) |
| 🗂️ Careers Explorer | Deep-dive cards with 6 tabs of detail per career track |
| 🗺️ Skill Roadmap Planner | 3-step interactive wizard — pick skills, set pace, get plan |
| ⚡ Demo Mode | `?demo=1` auto-fills the form for instant testing |
| 🌗 Dark / Light Theme | Toggle with localStorage persistence |
| 🔌 REST API | JSON endpoints for external integrations |
| 🛠️ Django Admin | Full admin panel with search, filters, and inline recommendations |

### 📄 AI Resume Screener
| Feature | Description |
|---|---|
| 🧠 TF-IDF Vectorization | Converts JD and resumes into weighted term vectors |
| 📐 Cosine Similarity | Mathematically ranks each resume against the job description |
| 🔍 Keyword Extraction | Detects top 20 keywords from the job description automatically |
| 🎯 Skill Gap Detection | Matches 35+ tech skills — shows what the candidate has and what's missing |
| 📊 Score Breakdown | Three separate scores: similarity, keyword coverage, skill match rate |
| 🏆 A–D Grade System | Excellent / Strong / Moderate / Weak match labels |
| 📋 Per-Resume Tabs | Skills, Keywords, and Score Breakdown tabs for every candidate |
| 💡 AI Verdict | Written assessment paragraph auto-generated for each resume |
| 🔁 Batch Screening | Upload and rank multiple resumes simultaneously |
| 📤 Drag & Drop Upload | Drop zone for PDF / DOCX resume files |
| 🔴 Live Skill Preview | Skills detected in the JD appear in real time as you type |

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

# 3. Install all dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env — set SECRET_KEY, DEBUG, etc.

# 5. Apply database migrations
python manage.py migrate

# 6. (Optional) Create an admin superuser
python manage.py createsuperuser

# 7. Collect static files
python manage.py collectstatic --noinput

# 8. Start the development server
python manage.py runserver
```

Open **http://127.0.0.1:8000** in your browser.  
Try the demo: **http://127.0.0.1:8000/profile/?demo=1**

---

## ⚙️ Environment Variables

All sensitive config lives in a `.env` file (development) or real environment variables (production).  
Copy `.env.example` → `.env` and fill in your values.

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
├── .env                                ← Your local secrets (git-ignored)
├── .env.example                        ← Copy to .env and fill in values
├── .gitignore
├── db.sqlite3                          ← Auto-created SQLite database
│
├── careercompass/                      ← Django project config
│   ├── settings.py                     ← All settings loaded from .env via python-decouple
│   ├── urls.py                         ← Root URL config (careers + screener)
│   └── wsgi.py
│
├── careers/                            ← Career recommendation app
│   ├── career_engine.py                ← Scoring engine + full career profile data
│   ├── career_matcher.py               ← Core scoring logic
│   ├── models.py                       ← StudentProfile + CareerRecommendation
│   ├── views.py                        ← Page views, API views, history, delete, shared result
│   ├── forms.py                        ← StudentProfileForm with validation
│   ├── urls.py                         ← All career + API URL routes
│   ├── admin.py                        ← Admin with list_display, search, filters
│   └── migrations/
│       ├── 0001_initial.py
│       └── 0002_studentprofile_share_token.py
│
├── resume_screener/                    ← Resume screening app
│   ├── views.py                        ← TF-IDF screener with skill + keyword analysis
│   ├── urls.py                         ← /screener/ route
│   ├── apps.py
│   └── uploads/                        ← Uploaded resume files (auto-created, git-ignored)
│
├── static/
│   ├── css/
│   │   ├── style.css                   ← Full design system (dark + light theme tokens)
│   │   ├── careers_list.css
│   │   ├── history.css
│   │   └── skill_roadmap.css
│   └── js/
│       ├── main.js                     ← Scroll reveal, 3D tilt, count-up, tabs, theme
│       ├── results.js                  ← Radar chart, score bars, tab logic
│       ├── careers_list.js             ← Career card expand, filter buttons
│       ├── history.js                  ← Live search, sort, AJAX delete, pagination
│       └── skill_roadmap.js            ← 3-step wizard, roadmap builder
│
├── staticfiles/                        ← WhiteNoise collected files (production)
│
└── templates/
    ├── careers/
    │   ├── base.html                   ← Shared nav, fonts, Chart.js, theme toggle
    │   ├── home.html                   ← Landing page with hero + feature cards
    │   ├── form.html                   ← Student profile input form + demo mode
    │   ├── results.html                ← Career results with tabs + radar chart
    │   ├── shared_result.html          ← Public read-only shareable result page
    │   ├── careers_list.html           ← Expandable career cards with 6 tabs each
    │   ├── history.html                ← Searchable, filterable, paginated history
    │   └── skill_roadmap.html          ← 3-step interactive skill planner
    └── resume_screener/
        └── screener.html               ← Enhanced resume screener with tabs + breakdown
```

---

## 🌐 URL Routes

### Career Recommendation

| URL | View | Description |
|---|---|---|
| `/` | `home` | Landing page |
| `/profile/` | `profile_form` | Student profile input form |
| `/profile/?demo=1` | `profile_form` | Auto-filled demo profile |
| `/analyze/` | `analyze` | POST — runs scoring, saves to DB |
| `/results/<uuid:token>/` | `shared_result` | Public shareable result page |
| `/careers/` | `careers_list` | Explore all 5 career tracks |
| `/history/` | `history` | All saved analyses |
| `/skill-roadmap/` | `skill_roadmap` | Interactive skill roadmap planner |
| `/delete-profile/<id>/` | `delete_profile` | POST — delete a saved profile |
| `/admin/` | Django admin | Manage profiles and recommendations |

### Resume Screener

| URL | View | Description |
|---|---|---|
| `/screener/` | `screener` | AI resume screener — upload & rank |

### REST API

| URL | Method | Description |
|---|---|---|
| `/api/careers/` | GET | All 5 career tracks as JSON |
| `/api/recommend/` | POST | Score a student profile, return ranked careers |

---

## 🔌 REST API

### `POST /api/recommend/`
Score a student profile and return ranked career recommendations.

```bash
curl -X POST http://127.0.0.1:8000/api/recommend/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Arjun Verma",
    "branch": "Computer Science Engineering",
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
  }
]
```

### `GET /api/careers/`
Returns all 5 career tracks with required skills, salary range, and demand level.

```bash
curl http://127.0.0.1:8000/api/careers/
```

---

## 🧠 Career Scoring Formula

```
Score = 18 + [
    skill_overlap  × weight_skill  +
    cgpa_norm      × weight_cgpa   +
    leetcode_norm  × weight_lc     +
    github_norm    × weight_gh
] × 80
```

Scores are clamped to **18–98** — no student ever gets 0.  
Each metric is normalised: CGPA / 10, LeetCode / 300, GitHub / 15.

**Career-specific weights:**

| Career | Skill | CGPA | LeetCode | GitHub |
|---|---|---|---|---|
| Software Development Engineer | 60% | 20% | 10% | 10% |
| Data Scientist / ML Engineer | 60% | 25% | 5% | 10% |
| Cloud / DevOps Engineer | 60% | 15% | 5% | 20% |
| Cybersecurity Engineer | 65% | 15% | 5% | 15% |
| Product Manager (Tech) | 50% | 20% | 10% | 20% |

The results page shows a **full score breakdown** — each component's exact point contribution so students know precisely what to improve.

---

## 🤖 Resume Screener — How It Works

```
1. Job Description  ──► TF-IDF Vectorizer ──► JD Vector
2. Resume Text      ──► TF-IDF Vectorizer ──► Resume Vector
3. Cosine Similarity(JD Vector, Resume Vector) → Match Score (0–100%)
4. Regex pattern matching → Skill extraction from 35+ known technologies
5. Top-N keyword extraction → Keyword overlap between JD and resume
```

**Score grades:**

| Score | Grade | Label |
|---|---|---|
| 75–100% | A | Excellent Match |
| 55–74% | B | Strong Match |
| 35–54% | C | Moderate Match |
| 0–34% | D | Weak Match |

**Supported resume formats:** `.pdf` (via PyMuPDF) · `.docx` (via python-docx)

---

## 🗂️ Career Tracks

| Career | Icon | Avg Salary | Demand | Difficulty |
|---|---|---|---|---|
| Software Development Engineer | 💻 | ₹8–35 LPA | Very High ↑ | Medium |
| Data Scientist / ML Engineer | 🤖 | ₹10–45 LPA | High ↑ | Hard |
| Cloud / DevOps Engineer | ☁️ | ₹9–40 LPA | High ↑ | Medium |
| Cybersecurity Engineer | 🔐 | ₹8–32 LPA | Growing ↑ | Hard |
| Product Manager (Tech) | 📋 | ₹12–50 LPA | Moderate → | Medium |

Each career includes: required skills · scoring weights · 5-phase 12-week roadmap · city-wise salary data (Bangalore, Hyderabad, Pune, Mumbai, Chennai, Remote) · top hiring companies · recommended certifications · day-in-life description · growth path · competency radar chart.

---

## 🗄️ Database Models

### `StudentProfile`

| Field | Type | Description |
|---|---|---|
| `name` | CharField | Student name |
| `branch` | CharField | Engineering branch (CSE / IT / ECE / EE / ME / DS) |
| `cgpa` | FloatField | CGPA out of 10 |
| `year` | CharField | Year of study |
| `leetcode` | IntegerField | LeetCode problems solved |
| `github` | IntegerField | Public GitHub repositories |
| `skills` | JSONField | List of selected skills |
| `share_token` | UUIDField | Auto-generated UUID for shareable links |
| `created_at` | DateTimeField | Auto timestamp |

### `CareerRecommendation`
Linked to `StudentProfile` via ForeignKey — cascades on delete.

| Field | Type | Description |
|---|---|---|
| `student` | ForeignKey | Links to StudentProfile |
| `career` | CharField | Career track name |
| `score` | IntegerField | Match score (18–98) |
| `rank` | IntegerField | Position in ranked results |
| `skills_have` | JSONField | Skills the student already has |
| `skills_missing` | JSONField | Skills the student needs to learn |
| `avg_salary` | CharField | Salary range string |
| `demand_trend` | CharField | Market demand indicator |

---

## 🎨 Frontend Design System

The frontend uses a custom design system called **"Deep Cosmos × Neon Precision"**:

- **Fonts:** Syne (headings) · DM Sans (body) · DM Mono (code) via Google Fonts
- **Theming:** Full CSS variable token system — dark and light modes with `[data-theme]`
- **Animations:** Scroll reveal · 3D card tilt · Count-up numbers · Progress bar fill · Button glow
- **Glassmorphism:** Floating sticky navbar with `backdrop-filter: blur(24px)`
- **Charts:** Chart.js 4.4 — radar chart + bar chart on results and careers pages
- **Background:** Animated cosmic grid + ambient orbs + starfield (dark mode only)

---

## 📋 Pages in Detail

### `/` — Home
Landing page with animated hero section, feature grid (6 cards), stats bar, and CTA buttons.

### `/profile/` — Career Analysis Form
Student profile form with:
- Name, branch, CGPA, year, LeetCode count, GitHub repos
- 30-skill chip selector with count badge
- Form validation with error display
- `?demo=1` auto-fills with a sample Arjun Verma profile

### `/analyze/` — Results Page
After submitting the form:
- Top 3 match cards with animated score bars
- Full tabbed breakdown per career: Overview · Skills · Roadmap · Salaries · Radar · Growth
- Score breakdown bar showing each component's contribution
- Share URL with UUID token
- "Analyse Again" and "View History" actions

### `/screener/` — Resume Screener
- Paste job description (live skill detection as you type)
- Drag-and-drop upload for multiple PDF / DOCX resumes
- Results ranked by cosine similarity score
- Each result card has 3 tabs: Skills · Keywords · Score Breakdown
- Summary bar: total screened · top score · skills detected · JD word count
- Sidebar: tips, score legend, how-it-works technical explanation

### `/careers/` — Career Tracks Explorer
- 5 expandable career cards with filter buttons
- Filter by: All · Very High Demand · High Demand · Top Salary · Difficulty
- Each card expands to **6 tabs**: Overview · Roles · Roadmap · Salaries · Skills · Radar

### `/history/` — Analysis History
- Live search (name, branch, career, skills)
- Filter by career track
- Sort by: newest / oldest / highest score / A–Z
- AJAX delete with confirm modal (no page reload)
- Pagination (8 per page)

### `/skill-roadmap/` — Skill Roadmap Planner
3-step interactive wizard:
1. **Pick Skills** — emoji chip tray, max 8 skills
2. **Timeline** — 4 / 8 / 12 / 16 weeks · beginner / intermediate / advanced
3. **Roadmap** — personalised week-by-week plan with tasks, resources, milestones

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11 · Django 4.x |
| Database | SQLite (dev) · PostgreSQL-ready |
| ML / NLP | scikit-learn 1.4 (TF-IDF, cosine similarity) |
| PDF Parsing | PyMuPDF (fitz) ≥ 1.23 |
| DOCX Parsing | python-docx ≥ 1.1 |
| File Handling | Werkzeug (secure_filename) |
| Frontend | HTML · CSS (custom design system) · Vanilla JS |
| Charts | Chart.js 4.4 (CDN) |
| Fonts | Google Fonts (Syne, DM Sans, DM Mono) |
| Static Files | WhiteNoise 6.6 (production serving + compression) |
| Production Server | Gunicorn 21.2 |
| Config Management | python-decouple 3.8 (.env support) |
| Version Control | Git |

---

## 🚀 Production Deployment (Render)

1. Push your repo to GitHub.
2. Create a new **Web Service** on [Render](https://render.com).
3. Set **Build Command:**
   ```bash
   pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
   ```
4. Set **Start Command:**
   ```bash
   gunicorn careercompass.wsgi
   ```
5. Add these **Environment Variables** in Render Dashboard → Environment:

   | Key | Value |
   |---|---|
   | `SECRET_KEY` | A strong random key (generate below) |
   | `DEBUG` | `False` |
   | `ALLOWED_HOSTS` | `your-app.onrender.com` |
   | `DB_ENGINE` | `sqlite3` |

WhiteNoise handles static file serving automatically — no separate CDN needed.

> **Note:** SQLite on Render resets on every deploy. For persistent data use `DB_ENGINE=postgresql` with a Render PostgreSQL add-on.

---

## 🚧 Future Improvements

- [ ] User authentication (login / signup / OAuth)
- [ ] PDF export of career analysis results
- [ ] Resume auto-parser — auto-fill skills from uploaded resume
- [ ] Persistent roadmap progress tracker (check off weekly tasks)
- [ ] Score history chart across multiple submissions
- [ ] More career tracks (UI/UX Design, Embedded Systems, Blockchain, Game Dev)
- [ ] Email notification with results summary
- [ ] PWA support — installable on mobile
- [ ] Comparison mode — view two career tracks side by side
- [ ] Resume screener history — save past screening sessions

---

## 👨‍💻 Author

Built by **Kartik** · CareerCompass · 2025–2026
