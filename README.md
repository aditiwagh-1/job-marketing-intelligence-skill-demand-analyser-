# Job Market Intelligence & Skill Demand Analytics

A full-stack, enterprise-grade **Job Market Intelligence, Skill Demand Analytics & Career Recommendation Platform** built with **Django**, **SQLite**, **Tailwind CSS**, **Pandas**, **NumPy**, **Scikit-Learn**, and **Chart.js**.

---

## 🌟 Key Features

### 1. 📊 Market Analytics Dashboard
- **6 Key KPI Metrics**: Total Jobs (520+), Tracked Tech Companies (40+), Distinct Tech Roles (15+), Average Salary (₹8.4 LPA), Remote Job Ratio (24%), and Top Demanded Skill (SQL / Python).
- **6 Interactive Dark-Themed Charts**:
  - Openings by Job Role
  - Openings by Tech Hub / City
  - Remote vs. Hybrid vs. On-site Distribution
  - Jobs by Seniority / Experience Level
  - Top 10 Hiring Companies
  - Top Demanded Skills (% frequency in job postings)

### 2. ⭐ Skill Demand Analytics
- Granular breakdown of top demanded skills across any selected job role (e.g. *Data Analyst*, *Data Scientist*, *Machine Learning Engineer*, *Full Stack Developer*, etc.).
- Visual Domain Radar Chart mapping intensity across **Programming**, **Databases**, **Visualization & BI**, **Analytics & Stats**, **Cloud & DevOps**, **AI/ML**, **Web & Frameworks**, and **Big Data Tools**.

### 3. 💰 Salary Intelligence & Compensation Insights
- Multi-dimensional salary filtering by **Role**, **Location**, and **Experience**.
- Real-time calculations of Average, Median (P50), Minimum, Maximum, and IQR 25th-75th percentiles.
- Interactive Salary Distribution Histogram, Experience vs Salary progression curve, and City-wise compensation comparisons.

### 4. 🧠 Signature Skill Gap Analyzer & Learning Roadmap
- Select your current technical proficiencies and choose a target career role.
- Dynamic calculation of **Skill Match Score %**, list of verified acquired skills, and identified missing gap tools.
- **Customized 4-Phase Learning Roadmap**:
  - Phase 1: Foundations & Core Tools
  - Phase 2: Data Wrangling & Scripting
  - Phase 3: Visual Analytics & Frameworks
  - Phase 4: Capstone Projects & Portfolio

### 5. 🎯 Career Recommendation & Content-Based Job Matching
- **Career Matching Engine**: Scores user compatibility across 15+ specialized tech career tracks.
- **Job Recommender**: Computes Jaccard / Cosine similarity between candidate skill set and live job requirements, ranking positions with clear matched vs missing skill highlights.

### 6. 🤖 Scikit-Learn Machine Learning Salary Predictor
- Random Forest regression pipeline predicting expected annual CTC (in ₹ LPA) based on role, years of experience, location, education, work setup, and skill multipliers.
- Computes estimated monthly take-home in INR and realistic compensation bounds.

### 7. 💼 Complete Job Search & User Profile System
- Multi-faceted job search with keyword matching, role, location, experience, work mode, and salary sliders.
- User registration, authentication, bookmarked jobs manager, and interactive skill tag manager.

---

## 🛠️ Technology Stack

| Layer | Technologies Used |
|---|---|
| **Backend** | Python 3.14, Django 6.1 |
| **Frontend** | Django Templates, Tailwind CSS 3, FontAwesome 6, Google Fonts (Outfit & Plus Jakarta Sans) |
| **Database** | SQLite + Django ORM (Indexed relational models) |
| **Data Analytics** | Pandas, NumPy |
| **Data Visualization** | Chart.js 4 (Custom dark themes) |
| **Machine Learning** | Scikit-Learn (Random Forest Regressor, ColumnTransformer, Pipeline), Joblib |

---

## 📁 Project Structure

```
job_market_intelligence/
│
├── manage.py
├── requirements.txt
├── README.md
│
├── job_market/                      # Django Project Configuration
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── core/                            # Landing & Platform Pages
│   ├── views.py
│   └── urls.py
│
├── jobs/                            # Job Listings & Search App
│   ├── models.py                    # Job, Company, Skill, SavedJob
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   └── management/commands/seed_jobs.py  # 520+ Realistic Job Postings
│
├── analytics/                       # Market & Skill Analytics App
│   ├── views.py
│   ├── services.py                  # Pandas statistical pipelines
│   └── urls.py
│
├── recommendations/                 # Intelligence & ML App
│   ├── views.py
│   ├── services.py                  # Skill gap & matching engine
│   ├── ml_engine.py                 # Scikit-learn Random Forest model
│   ├── urls.py
│   └── ml_models/                   # Trained .joblib model files
│
├── accounts/                        # User Profiles & Auth App
│   ├── models.py                    # UserProfile, UserSkill
│   ├── views.py
│   ├── forms.py
│   └── urls.py
│
├── templates/                       # HTML5 Django Templates
│   ├── base.html
│   ├── core/
│   ├── jobs/
│   ├── analytics/
│   ├── recommendations/
│   └── accounts/
│
├── static/                          # CSS & JS Assets
│   ├── css/custom.css
│   └── js/
│       ├── main.js
│       └── charts.js
│
└── notebooks/                       # Data Science EDA
    ├── data_cleaning.ipynb
    └── analysis.ipynb
```

---

## 🚀 Quick Setup & Run Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Apply Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Seed Realistic Market Dataset
```bash
python manage.py seed_jobs
```
*Populates 520+ jobs across 40 top companies, 71 skills, and demo accounts.*

### 4. Run the Development Server
```bash
python manage.py runserver
```

Open your browser at `http://127.0.0.1:8000/`

---

## 👤 Preloaded Demo Accounts

| Account Type | Username | Password | Notes |
|---|---|---|---|
| **Demo User** | `demo_user` | `demopassword123` | Pre-configured Data Analyst profile with Python, SQL, Excel, and Power BI skills |
| **Administrator** | `admin` | `adminpassword123` | Full Django admin access at `/admin/` |

---

## 📜 License
Open Source & Educational Use.
