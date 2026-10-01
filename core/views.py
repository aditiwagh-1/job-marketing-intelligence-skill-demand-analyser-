from django.shortcuts import render, redirect
from django.db.models import Avg, Count
from jobs.models import Job, Company, Skill


def home(request):
    total_jobs = Job.objects.count()
    total_companies = Company.objects.count()
    unique_roles = Job.objects.values('role_category').distinct().count()
    unique_skills = Skill.objects.count()
    
    avg_salary_val = Job.objects.aggregate(avg=Avg('salary_avg'))['avg'] or 8.4
    avg_salary = round(avg_salary_val, 1)

    top_roles = Job.objects.values('role_category').annotate(
        job_count=Count('id'),
        avg_sal=Avg('salary_avg')
    ).order_by('-job_count')[:6]

    top_skills = Skill.objects.annotate(
        job_count=Count('jobs')
    ).order_by('-job_count')[:10]

    featured_jobs = Job.objects.select_related('company').prefetch_related('skills')[:6]

    context = {
        'total_jobs': total_jobs,
        'total_companies': total_companies,
        'unique_roles': unique_roles,
        'unique_skills': unique_skills,
        'avg_salary': avg_salary,
        'top_roles': top_roles,
        'top_skills': top_skills,
        'featured_jobs': featured_jobs,
    }
    return render(request, 'core/home.html', context)


def about(request):
    return render(request, 'core/about.html')
