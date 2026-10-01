from django.db.models import Count
from jobs.models import Job, Skill, Company


ROLE_SKILL_ROADMAPS = {
    'Data Analyst': [
        {'phase': 'Phase 1: Foundations', 'title': 'Spreadsheet Modeling & Basic SQL', 'skills': ['Excel', 'SQL'], 'desc': 'Master advanced formulas, pivot tables, relational database fundamentals, joins, and aggregations.', 'duration': '3-4 Weeks'},
        {'phase': 'Phase 2: Programming', 'title': 'Python & Data Wrangling', 'skills': ['Python', 'Pandas', 'NumPy'], 'desc': 'Learn Python data structures, DataFrame transformations, data cleaning, and exploratory data analysis.', 'duration': '4-5 Weeks'},
        {'phase': 'Phase 3: Visual Analytics', 'title': 'Interactive BI Dashboards', 'skills': ['Power BI', 'Tableau', 'Data Analysis'], 'desc': 'Build executive dashboards, KPI monitors, DAX formulas, and visual storytelling reports.', 'duration': '3-4 Weeks'},
        {'phase': 'Phase 4: Advanced & Strategy', 'title': 'Statistical Testing & Portfolio', 'skills': ['Statistics', 'A/B Testing'], 'desc': 'Conduct hypothesis testing, experiment design, and build end-to-end portfolio case studies on GitHub.', 'duration': '3 Weeks'},
    ],
    'Data Scientist': [
        {'phase': 'Phase 1: Math & Code', 'title': 'Mathematical Foundations & Python', 'skills': ['Python', 'Statistics', 'Linear Algebra', 'SQL'], 'desc': 'Rigorous statistics, probability distributions, matrix operations, and SQL querying.', 'duration': '4-6 Weeks'},
        {'phase': 'Phase 2: Core ML', 'title': 'Classical Machine Learning', 'skills': ['Scikit-learn', 'Pandas', 'Predictive Modeling'], 'desc': 'Regression, classification, decision trees, random forests, cross-validation, and hyperparameter tuning.', 'duration': '5-6 Weeks'},
        {'phase': 'Phase 3: Deep Tech', 'title': 'Deep Learning & NLP', 'skills': ['PyTorch', 'TensorFlow', 'NLP', 'Deep Learning'], 'desc': 'Neural networks, embeddings, transformers, natural language pipelines, and computer vision.', 'duration': '6-8 Weeks'},
        {'phase': 'Phase 4: Production', 'title': 'MLOps & Cloud Deployment', 'skills': ['Docker', 'AWS', 'MLOps'], 'desc': 'Containerizing models, REST API endpoints with FastAPI, CI/CD, and model monitoring in cloud.', 'duration': '4 Weeks'},
    ],
    'Business Intelligence Analyst': [
        {'phase': 'Phase 1: Data Foundations', 'title': 'Enterprise SQL & Excel', 'skills': ['SQL', 'Excel', 'Data Analysis'], 'desc': 'Complex window functions, CTEs, data warehousing star schemas, and spreadsheet modeling.', 'duration': '3-4 Weeks'},
        {'phase': 'Phase 2: BI Platforms', 'title': 'Power BI & Tableau Mastery', 'skills': ['Power BI', 'Tableau', 'Looker'], 'desc': 'Semantic layer modeling, DAX measures, automated refresh pipelines, and interactive drill-downs.', 'duration': '4-5 Weeks'},
        {'phase': 'Phase 3: Data Warehousing', 'title': 'Cloud Warehousing & ETL', 'skills': ['Snowflake', 'PostgreSQL', 'dbt'], 'desc': 'Data modeling, schema design, and transformation workflows.', 'duration': '4 Weeks'},
        {'phase': 'Phase 4: Executive Insights', 'title': 'Business Strategy & Metrics', 'skills': ['Data Governance', 'A/B Testing'], 'desc': 'Defining North Star metrics, stakeholder reporting, and enterprise governance.', 'duration': '2-3 Weeks'},
    ],
    'Machine Learning Engineer': [
        {'phase': 'Phase 1: Foundations', 'title': 'Python, Algorithms & Data', 'skills': ['Python', 'SQL', 'Git', 'Linux'], 'desc': 'Data structures, algorithm complexity, software engineering principles, and database access.', 'duration': '4 Weeks'},
        {'phase': 'Phase 2: Modeling', 'title': 'Applied ML & Deep Learning', 'skills': ['Scikit-learn', 'PyTorch', 'Deep Learning'], 'desc': 'Gradient boosting, convolutional nets, transformers, and model evaluation techniques.', 'duration': '6 Weeks'},
        {'phase': 'Phase 3: LLMs & Modern AI', 'title': 'Generative AI & LLMs', 'skills': ['Large Language Models', 'LangChain', 'NLP'], 'desc': 'RAG pipelines, vector databases, fine-tuning open source models, and prompt engineering.', 'duration': '4-5 Weeks'},
        {'phase': 'Phase 4: MLOps & Cloud', 'title': 'Production Infrastructure', 'skills': ['Docker', 'Kubernetes', 'MLOps', 'AWS', 'FastAPI'], 'desc': 'Model serving with low latency, model registries, automated retraining, and scaling.', 'duration': '5-6 Weeks'},
    ],
    'Full Stack Developer': [
        {'phase': 'Phase 1: Frontend Core', 'title': 'Modern JavaScript & React', 'skills': ['JavaScript', 'TypeScript', 'React', 'Tailwind CSS'], 'desc': 'Component architecture, state management, responsive styling, and modern React hooks.', 'duration': '4-6 Weeks'},
        {'phase': 'Phase 2: Backend Architecture', 'title': 'APIs & Server Logic', 'skills': ['Node.js', 'Python', 'REST API', 'Django', 'FastAPI'], 'desc': 'RESTful API design, authentication, middleware, and business logic routing.', 'duration': '5 Weeks'},
        {'phase': 'Phase 3: Databases & Cache', 'title': 'Relational & NoSQL Storage', 'skills': ['SQL', 'PostgreSQL', 'MongoDB', 'Redis'], 'desc': 'Data schemas, ORM queries, indexing, caching strategies, and performance tuning.', 'duration': '4 Weeks'},
        {'phase': 'Phase 4: DevOps & Ship', 'title': 'Deployment & Cloud', 'skills': ['Docker', 'Git', 'CI/CD', 'AWS'], 'desc': 'Containerization, automated build pipelines, production deployment, and monitoring.', 'duration': '3-4 Weeks'},
    ],
}


def calculate_skill_gap(user_skill_names, target_role):
    """
    Performs full skill gap analysis against the target job role.
    Computes match %, matched skills, missing skills, and dynamic roadmap.
    """
    user_skills_set = set([s.strip().lower() for s in user_skill_names if s.strip()])
    
    # Get all jobs for this role to determine required skills ranked by market demand
    role_jobs = Job.objects.filter(role_category=target_role)
    if not role_jobs.exists():
        role_jobs = Job.objects.all()

    total_role_jobs = max(role_jobs.count(), 1)
    
    role_skills_qs = Skill.objects.filter(jobs__in=role_jobs).annotate(
        req_count=Count('jobs')
    ).order_by('-req_count')

    # Top required skills for this role (up to 12 most frequent)
    required_skills_list = []
    matched_skills = []
    missing_skills = []

    for s in role_skills_qs[:10]:
        frequency_pct = round((s.req_count / total_role_jobs) * 100)
        skill_info = {
            'id': s.id,
            'name': s.name,
            'category': s.get_category_display(),
            'icon': s.icon,
            'importance_weight': s.importance_weight,
            'market_demand_pct': frequency_pct,
        }
        required_skills_list.append(skill_info)

        if s.name.lower() in user_skills_set:
            matched_skills.append(skill_info)
        else:
            missing_skills.append(skill_info)

    total_req = len(required_skills_list)
    matched_count = len(matched_skills)
    match_percentage = round((matched_count / max(total_req, 1)) * 100) if total_req > 0 else 0

    # Skill Readiness Tier
    if match_percentage >= 80:
        readiness_label = 'Job Ready'
        readiness_color = 'emerald'
        readiness_desc = 'Your skill set strongly aligns with current industry expectations for this role! You are ready to apply for top openings.'
    elif match_percentage >= 50:
        readiness_label = 'Intermediate Match'
        readiness_color = 'amber'
        readiness_desc = 'You possess good foundational skills. Bridging 2-3 key missing skills will significantly boost your interview callback rate.'
    else:
        readiness_label = 'Foundational / Upskilling Needed'
        readiness_color = 'rose'
        readiness_desc = 'You have promising baseline skills, but this role requires additional core technical tools. Follow the customized learning path below.'

    # Get tailored learning roadmap
    roadmap = ROLE_SKILL_ROADMAPS.get(target_role, ROLE_SKILL_ROADMAPS['Data Analyst'])
    
    # Mark which roadmap milestones have been acquired
    processed_roadmap = []
    for step in roadmap:
        step_skills = step['skills']
        step_matched = [sk for sk in step_skills if sk.lower() in user_skills_set]
        step_progress = round((len(step_matched) / max(len(step_skills), 1)) * 100)
        processed_roadmap.append({
            'phase': step['phase'],
            'title': step['title'],
            'skills': step_skills,
            'desc': step['desc'],
            'duration': step['duration'],
            'step_progress': step_progress,
            'is_completed': step_progress == 100,
        })

    estimated_weeks = max(len(missing_skills) * 2, 2)

    return {
        'target_role': target_role,
        'user_skills_count': len(user_skill_names),
        'required_count': total_req,
        'matched_count': matched_count,
        'missing_count': len(missing_skills),
        'match_percentage': match_percentage,
        'readiness_label': readiness_label,
        'readiness_color': readiness_color,
        'readiness_desc': readiness_desc,
        'matched_skills': matched_skills,
        'missing_skills': missing_skills,
        'required_skills': required_skills_list,
        'roadmap': processed_roadmap,
        'estimated_weeks': estimated_weeks,
    }


def get_career_recommendations(user_skill_names):
    """
    Ranks top career paths based on overlap with user's skill set.
    """
    user_skills_set = set([s.strip().lower() for s in user_skill_names if s.strip()])
    
    roles = Job.objects.values_list('role_category', flat=True).distinct().order_by('role_category')
    recommendations = []

    for role in roles:
        role_jobs = Job.objects.filter(role_category=role)
        total_jobs = role_jobs.count()
        avg_sal = round(role_jobs.aggregate(avg=Count('salary_avg'))['avg'] or 0.0, 1)

        # Get top 8 skills required for this role
        top_skills = list(Skill.objects.filter(jobs__in=role_jobs).annotate(
            cnt=Count('jobs')
        ).order_by('-cnt')[:8])

        if not top_skills:
            continue

        matched = [s for s in top_skills if s.name.lower() in user_skills_set]
        missing = [s for s in top_skills if s.name.lower() not in user_skills_set]
        
        match_score = round((len(matched) / len(top_skills)) * 100)

        # Growth & Fit Tier
        if match_score >= 80:
            fit_badge = 'Excellent Fit'
            badge_color = 'emerald'
        elif match_score >= 50:
            fit_badge = 'Strong Potential'
            badge_color = 'cyan'
        elif match_score >= 30:
            fit_badge = 'Moderate Pivot'
            badge_color = 'amber'
        else:
            fit_badge = 'Career Stretch'
            badge_color = 'slate'

        recommendations.append({
            'role': role,
            'match_score': match_score,
            'fit_badge': fit_badge,
            'badge_color': badge_color,
            'total_openings': total_jobs,
            'matched_skills': [s.name for s in matched],
            'missing_skills': [s.name for s in missing[:4]],
            'top_skills': [s.name for s in top_skills[:5]],
        })

    # Sort descending by match score
    recommendations.sort(key=lambda x: (x['match_score'], x['total_openings']), reverse=True)
    return recommendations


def get_job_recommendations(user_skill_names, target_role=None, preferred_location=None, limit=12):
    """
    Ranks individual job listings based on content skill match with the user.
    """
    user_skills_set = set([s.strip().lower() for s in user_skill_names if s.strip()])
    
    jobs_qs = Job.objects.select_related('company').prefetch_related('skills').filter(is_active=True)
    
    if target_role and target_role != 'All':
        jobs_qs = jobs_qs.filter(role_category=target_role)
    if preferred_location and preferred_location not in ['All', 'Any']:
        jobs_qs = jobs_qs.filter(location__icontains=preferred_location)

    scored_jobs = []
    for job in jobs_qs:
        job_skills = list(job.skills.all())
        if not job_skills:
            continue

        matched_skills = [s for s in job_skills if s.name.lower() in user_skills_set]
        missing_skills = [s for s in job_skills if s.name.lower() not in user_skills_set]

        match_score = round((len(matched_skills) / len(job_skills)) * 100) if job_skills else 0

        scored_jobs.append({
            'job': job,
            'match_score': match_score,
            'matched_skills': matched_skills,
            'missing_skills': missing_skills,
            'matched_count': len(matched_skills),
            'total_skills_count': len(job_skills),
        })

    # Sort descending by match score, then salary
    scored_jobs.sort(key=lambda x: (x['match_score'], x['job'].salary_avg), reverse=True)
    return scored_jobs[:limit]
