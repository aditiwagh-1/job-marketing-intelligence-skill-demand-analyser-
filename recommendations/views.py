from django.shortcuts import render
from jobs.models import Skill, Job
from .services import (
    calculate_skill_gap,
    get_career_recommendations,
    get_job_recommendations,
)
from .ml_engine import predict_salary


def skill_gap(request):
    all_skills = Skill.objects.all().order_by('category', 'name')
    all_roles = list(Job.objects.values_list('role_category', flat=True).distinct().order_by('role_category'))

    # Determine default or submitted user skills
    if request.method == 'POST':
        selected_skills = request.POST.getlist('skills')
        target_role = request.POST.get('target_role', 'Data Analyst')
    else:
        target_role = request.GET.get('target_role')
        req_skills = request.GET.getlist('skills')
        if req_skills:
            selected_skills = req_skills
        elif request.user.is_authenticated and hasattr(request.user, 'profile'):
            selected_skills = list(request.user.profile.skills.values_list('name', flat=True))
            if not target_role:
                target_role = request.user.profile.target_role or 'Data Analyst'
        else:
            selected_skills = ['SQL', 'Python', 'Excel', 'Power BI']
            if not target_role:
                target_role = 'Data Analyst'

    if not target_role:
        target_role = 'Data Analyst'

    gap_results = calculate_skill_gap(selected_skills, target_role)

    context = {
        'all_skills': all_skills,
        'all_roles': all_roles,
        'selected_skills': selected_skills,
        'selected_role': target_role,
        'gap': gap_results,
    }
    return render(request, 'recommendations/skill_gap.html', context)


def career_recommendations(request):
    if request.user.is_authenticated and hasattr(request.user, 'profile'):
        user_skills = list(request.user.profile.skills.values_list('name', flat=True))
    else:
        user_skills = ['SQL', 'Python', 'Excel', 'Power BI', 'Data Analysis']

    custom_skills = request.GET.getlist('skills')
    if custom_skills:
        user_skills = custom_skills

    careers = get_career_recommendations(user_skills)
    all_skills = Skill.objects.all().order_by('name')

    context = {
        'user_skills': user_skills,
        'careers': careers,
        'all_skills': all_skills,
    }
    return render(request, 'recommendations/career_recommendations.html', context)


def job_recommendations(request):
    if request.user.is_authenticated and hasattr(request.user, 'profile'):
        user_skills = list(request.user.profile.skills.values_list('name', flat=True))
        preferred_loc = request.user.profile.preferred_location
    else:
        user_skills = ['SQL', 'Python', 'Excel', 'Power BI', 'Data Analysis']
        preferred_loc = 'All'

    role_filter = request.GET.get('role', 'All')
    loc_filter = request.GET.get('location', preferred_loc)

    matched_jobs = get_job_recommendations(user_skills, role_filter, loc_filter, limit=12)
    all_roles = ['All'] + list(Job.objects.values_list('role_category', flat=True).distinct().order_by('role_category'))
    all_locations = ['All', 'Bengaluru', 'Mumbai', 'Pune', 'Hyderabad', 'Delhi-NCR', 'Gurugram', 'Noida', 'Chennai', 'Remote']

    context = {
        'user_skills': user_skills,
        'matched_jobs': matched_jobs,
        'all_roles': all_roles,
        'all_locations': all_locations,
        'selected_role': role_filter,
        'selected_location': loc_filter,
    }
    return render(request, 'recommendations/job_recommendations.html', context)


def salary_predictor(request):
    all_roles = list(Job.objects.values_list('role_category', flat=True).distinct().order_by('role_category'))
    all_locations = ['Bengaluru', 'Mumbai', 'Pune', 'Hyderabad', 'Delhi-NCR', 'Gurugram', 'Noida', 'Chennai', 'Remote']
    all_educations = ["Bachelor's Degree", "Master's Degree", "MBA", "Doctorate / PhD", "Self-Taught / Bootcamp"]
    all_work_modes = ['Hybrid', 'Remote', 'On-site']
    all_skills = Skill.objects.all().order_by('name')

    # Defaults
    role = request.POST.get('role') or request.GET.get('role', 'Data Analyst')
    try:
        exp_years = float(request.POST.get('experience_years') or request.GET.get('experience_years', 2.0))
    except ValueError:
        exp_years = 2.0
        
    location = request.POST.get('location') or request.GET.get('location', 'Bengaluru')
    education = request.POST.get('education') or request.GET.get('education', "Bachelor's Degree")
    work_mode = request.POST.get('work_mode') or request.GET.get('work_mode', 'Hybrid')

    if request.method == 'POST':
        selected_skills = request.POST.getlist('skills')
    else:
        if request.user.is_authenticated and hasattr(request.user, 'profile'):
            selected_skills = list(request.user.profile.skills.values_list('name', flat=True))
        else:
            selected_skills = ['SQL', 'Python', 'Power BI']

    prediction = predict_salary(
        role_category=role,
        years_of_experience=exp_years,
        location=location,
        education=education,
        work_mode=work_mode,
        user_skills=selected_skills
    )

    context = {
        'all_roles': all_roles,
        'all_locations': all_locations,
        'all_educations': all_educations,
        'all_work_modes': all_work_modes,
        'all_skills': all_skills,
        'selected_role': role,
        'selected_exp': exp_years,
        'selected_loc': location,
        'selected_edu': education,
        'selected_mode': work_mode,
        'selected_skills': selected_skills,
        'prediction': prediction,
    }
    return render(request, 'recommendations/salary_predictor.html', context)
