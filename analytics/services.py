import pandas as pd
import numpy as np
from django.db.models import Count, Avg, Min, Max, Q
from jobs.models import Job, Company, Skill


def get_kpi_summary():
    """Returns high-level KPI metrics for the analytics dashboard."""
    total_jobs = Job.objects.count()
    total_companies = Company.objects.count()
    unique_roles = Job.objects.values('role_category').distinct().count()
    
    salary_stats = Job.objects.aggregate(
        avg_salary=Avg('salary_avg'),
        min_salary=Min('salary_min'),
        max_salary=Max('salary_max'),
    )
    avg_salary = round(salary_stats['avg_salary'] or 0.0, 2)
    
    remote_jobs_count = Job.objects.filter(work_mode='Remote').count()
    remote_percentage = round((remote_jobs_count / total_jobs * 100), 1) if total_jobs > 0 else 0.0
    
    # Top demanded skill
    top_skill_obj = Skill.objects.annotate(
        job_count=Count('jobs')
    ).order_by('-job_count').first()
    
    top_skill_name = top_skill_obj.name if top_skill_obj else 'SQL'
    top_skill_count = top_skill_obj.job_count if top_skill_obj else 0
    top_skill_percentage = round((top_skill_count / total_jobs * 100), 1) if total_jobs > 0 else 0

    return {
        'total_jobs': total_jobs,
        'total_companies': total_companies,
        'unique_roles': unique_roles,
        'avg_salary': avg_salary,
        'min_salary': round(salary_stats['min_salary'] or 0, 1),
        'max_salary': round(salary_stats['max_salary'] or 0, 1),
        'remote_jobs_count': remote_jobs_count,
        'remote_percentage': remote_percentage,
        'top_skill_name': top_skill_name,
        'top_skill_percentage': top_skill_percentage,
    }


def get_dashboard_charts_data():
    """Generates structured chart datasets for Chart.js on the main dashboard."""
    total_jobs = Job.objects.count()
    if total_jobs == 0:
        return {}

    # Chart 1: Jobs by Role Category
    roles_qs = Job.objects.values('role_category').annotate(
        count=Count('id'),
        avg_salary=Avg('salary_avg')
    ).order_by('-count')
    
    role_labels = [r['role_category'] for r in roles_qs]
    role_counts = [r['count'] for r in roles_qs]
    role_salaries = [round(r['avg_salary'], 1) for r in roles_qs]

    # Chart 2: Jobs by Location
    loc_qs = Job.objects.values('location').annotate(
        count=Count('id')
    ).order_by('-count')[:8]
    
    loc_labels = [l['location'] for l in loc_qs]
    loc_counts = [l['count'] for l in loc_qs]

    # Chart 3: Remote vs Hybrid vs On-site
    mode_qs = Job.objects.values('work_mode').annotate(
        count=Count('id')
    ).order_by('work_mode')
    
    mode_labels = [m['work_mode'] for m in mode_qs]
    mode_counts = [m['count'] for m in mode_qs]

    # Chart 4: Jobs by Experience Level
    exp_order = ['Entry Level', 'Mid Level', 'Senior Level', 'Lead / Principal']
    exp_qs = {e['experience_level']: e['count'] for e in Job.objects.values('experience_level').annotate(count=Count('id'))}
    exp_labels = exp_order
    exp_counts = [exp_qs.get(lvl, 0) for lvl in exp_order]

    # Chart 5: Top Hiring Companies
    comp_qs = Company.objects.annotate(
        job_count=Count('jobs')
    ).order_by('-job_count')[:10]
    
    comp_labels = [c.name for c in comp_qs]
    comp_counts = [c.job_count for c in comp_qs]

    # Chart 6: Top Demanded Skills
    skills_qs = Skill.objects.annotate(
        job_count=Count('jobs')
    ).order_by('-job_count')[:12]
    
    skill_labels = [s.name for s in skills_qs]
    skill_percentages = [round((s.job_count / total_jobs) * 100, 1) for s in skills_qs]

    return {
        'roles': {'labels': role_labels, 'counts': role_counts, 'salaries': role_salaries},
        'locations': {'labels': loc_labels, 'counts': loc_counts},
        'work_modes': {'labels': mode_labels, 'counts': mode_counts},
        'experience': {'labels': exp_labels, 'counts': exp_counts},
        'companies': {'labels': comp_labels, 'counts': comp_counts},
        'skills': {'labels': skill_labels, 'percentages': skill_percentages},
    }


def get_skill_demand_analytics(selected_role=None):
    """
    Returns in-depth skill demand analysis, both overall and role-specific,
    categorized by skill domains.
    """
    all_roles = list(Job.objects.values_list('role_category', flat=True).distinct().order_by('role_category'))
    
    jobs_filter = Job.objects.all()
    if selected_role and selected_role in all_roles:
        jobs_filter = jobs_filter.filter(role_category=selected_role)
    else:
        selected_role = 'All Roles'
    
    total_role_jobs = jobs_filter.count()
    if total_role_jobs == 0:
        total_role_jobs = 1

    # Skills demand ranking
    skills_stats = Skill.objects.filter(jobs__in=jobs_filter).annotate(
        frequency=Count('jobs')
    ).order_by('-frequency')

    top_skills_list = []
    category_grouped = {
        'programming': {'title': 'Programming Languages', 'icon': 'fa-code', 'skills': []},
        'database': {'title': 'Databases & Warehousing', 'icon': 'fa-database', 'skills': []},
        'visualization': {'title': 'Visualization & BI', 'icon': 'fa-chart-pie', 'skills': []},
        'analytics': {'title': 'Analytics & Statistics', 'icon': 'fa-magnifying-glass-chart', 'skills': []},
        'cloud_devops': {'title': 'Cloud & DevOps', 'icon': 'fa-cloud', 'skills': []},
        'ai_ml': {'title': 'AI & Machine Learning', 'icon': 'fa-brain', 'skills': []},
        'web_mobile': {'title': 'Web & Frameworks', 'icon': 'fa-cubes', 'skills': []},
        'tools_other': {'title': 'Big Data & Tools', 'icon': 'fa-screwdriver-wrench', 'skills': []},
    }

    for s in skills_stats:
        percentage = round((s.frequency / total_role_jobs) * 100, 1)
        skill_item = {
            'id': s.id,
            'name': s.name,
            'category': s.category,
            'icon': s.icon,
            'frequency': s.frequency,
            'percentage': percentage,
        }
        top_skills_list.append(skill_item)
        if s.category in category_grouped:
            category_grouped[s.category]['skills'].append(skill_item)

    # Categories Radar / Bar summary
    category_labels = []
    category_averages = []
    for cat_key, cat_data in category_grouped.items():
        if cat_data['skills']:
            avg_pct = round(sum(item['percentage'] for item in cat_data['skills']) / len(cat_data['skills']), 1)
        else:
            avg_pct = 0.0
        category_labels.append(cat_data['title'])
        category_averages.append(avg_pct)

    return {
        'all_roles': all_roles,
        'selected_role': selected_role,
        'total_jobs_analyzed': total_role_jobs,
        'top_skills': top_skills_list[:15],
        'category_grouped': category_grouped,
        'category_radar': {
            'labels': category_labels,
            'scores': category_averages,
        }
    }


def get_salary_intelligence_data(selected_role='All', selected_location='All', selected_experience='All'):
    """
    Computes statistical salary metrics, distribution curves, experience progression,
    and location comparison.
    """
    qs = Job.objects.all()
    
    if selected_role and selected_role != 'All':
        qs = qs.filter(role_category=selected_role)
    if selected_location and selected_location != 'All':
        qs = qs.filter(location=selected_location)
    if selected_experience and selected_experience != 'All':
        qs = qs.filter(experience_level=selected_experience)

    total_matched = qs.count()
    if total_matched == 0:
        # Fallback to general stats if filter returns empty
        qs = Job.objects.all()
        total_matched = qs.count()

    # Convert queryset to Pandas DataFrame for advanced statistical analysis
    jobs_data = list(qs.values('id', 'role_category', 'location', 'experience_level', 'salary_min', 'salary_max', 'salary_avg'))
    df = pd.DataFrame(jobs_data)

    avg_salary = round(float(df['salary_avg'].mean()), 2)
    median_salary = round(float(df['salary_avg'].median()), 2)
    min_salary = round(float(df['salary_min'].min()), 1)
    max_salary = round(float(df['salary_max'].max()), 1)
    p25 = round(float(df['salary_avg'].quantile(0.25)), 1)
    p75 = round(float(df['salary_avg'].quantile(0.75)), 1)

    # Salary Distribution Histogram Bins
    bins = [0, 6, 10, 15, 20, 30, 45, 60, 100]
    bin_labels = ['< ₹6L', '₹6L - ₹10L', '₹10L - ₹15L', '₹15L - ₹20L', '₹20L - ₹30L', '₹30L - ₹45L', '₹45L - ₹60L', '₹60L+']
    df['salary_bin'] = pd.cut(df['salary_avg'], bins=bins, labels=bin_labels, right=False)
    dist_counts = df['salary_bin'].value_counts().reindex(bin_labels, fill_value=0).tolist()

    # Salary by Experience Level Progression
    exp_order = ['Entry Level', 'Mid Level', 'Senior Level', 'Lead / Principal']
    exp_summary = df.groupby('experience_level')['salary_avg'].agg(['mean', 'min', 'max']).reindex(exp_order).fillna(0)
    exp_labels = exp_order
    exp_avg_salaries = [round(val, 1) for val in exp_summary['mean'].tolist()]
    exp_min_salaries = [round(val, 1) for val in exp_summary['min'].tolist()]
    exp_max_salaries = [round(val, 1) for val in exp_summary['max'].tolist()]

    # Salary by Location
    loc_summary = df.groupby('location')['salary_avg'].mean().sort_values(ascending=False)
    loc_labels = list(loc_summary.index)[:8]
    loc_salaries = [round(float(val), 1) for val in loc_summary.values][:8]

    # Dropdown options
    all_roles = ['All'] + list(Job.objects.values_list('role_category', flat=True).distinct().order_by('role_category'))
    all_locations = ['All'] + list(Job.objects.values_list('location', flat=True).distinct().order_by('location'))
    all_experiences = ['All', 'Entry Level', 'Mid Level', 'Senior Level', 'Lead / Principal']

    return {
        'total_matched': total_matched,
        'avg_salary': avg_salary,
        'median_salary': median_salary,
        'min_salary': min_salary,
        'max_salary': max_salary,
        'p25': p25,
        'p75': p75,
        'distribution': {
            'labels': bin_labels,
            'counts': dist_counts,
        },
        'experience_salary': {
            'labels': exp_labels,
            'avg': exp_avg_salaries,
            'min': exp_min_salaries,
            'max': exp_max_salaries,
        },
        'location_salary': {
            'labels': loc_labels,
            'salaries': loc_salaries,
        },
        'all_roles': all_roles,
        'all_locations': all_locations,
        'all_experiences': all_experiences,
        'selected_role': selected_role,
        'selected_location': selected_location,
        'selected_experience': selected_experience,
    }


def get_location_insights_data():
    """Detailed analytics on city-wise tech hubs, average salaries, and remote trends."""
    locations_qs = Job.objects.values('location').annotate(
        job_count=Count('id'),
        avg_salary=Avg('salary_avg'),
        remote_count=Count('id', filter=Q(work_mode='Remote')),
        hybrid_count=Count('id', filter=Q(work_mode='Hybrid')),
        onsite_count=Count('id', filter=Q(work_mode='On-site')),
    ).order_by('-job_count')

    locations_list = []
    for loc in locations_qs:
        total = loc['job_count']
        locations_list.append({
            'name': loc['location'],
            'job_count': total,
            'avg_salary': round(loc['avg_salary'] or 0.0, 1),
            'remote_pct': round((loc['remote_count'] / total) * 100, 1) if total > 0 else 0,
            'hybrid_pct': round((loc['hybrid_count'] / total) * 100, 1) if total > 0 else 0,
            'onsite_pct': round((loc['onsite_count'] / total) * 100, 1) if total > 0 else 0,
        })

    return {
        'locations': locations_list,
        'top_locations_chart': {
            'labels': [l['name'] for l in locations_list[:8]],
            'counts': [l['job_count'] for l in locations_list[:8]],
            'salaries': [l['avg_salary'] for l in locations_list[:8]],
        }
    }
