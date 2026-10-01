from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, Avg
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Job, Company, Skill, SavedJob
from .forms import JobFilterForm


def job_list(request):
    form = JobFilterForm(request.GET)
    jobs_qs = Job.objects.select_related('company').prefetch_related('skills').filter(is_active=True)

    # 1. Search Query
    q = request.GET.get('q', '').strip()
    if q:
        jobs_qs = jobs_qs.filter(
            Q(title__icontains=q) |
            Q(company__name__icontains=q) |
            Q(skills__name__icontains=q) |
            Q(description__icontains=q) |
            Q(role_category__icontains=q)
        ).distinct()

    # 2. Filter by Role Category
    role = request.GET.get('role', '').strip()
    if role and role != 'All':
        jobs_qs = jobs_qs.filter(role_category=role)

    # 3. Filter by Location
    location = request.GET.get('location', '').strip()
    if location and location != 'All':
        jobs_qs = jobs_qs.filter(location__icontains=location)

    # 4. Filter by Experience
    experience = request.GET.get('experience', '').strip()
    if experience and experience != 'All':
        jobs_qs = jobs_qs.filter(experience_level=experience)

    # 5. Filter by Work Mode
    work_mode = request.GET.get('work_mode', '').strip()
    if work_mode and work_mode != 'All':
        jobs_qs = jobs_qs.filter(work_mode=work_mode)

    # 6. Filter by Employment Type
    emp_type = request.GET.get('employment_type', '').strip()
    if emp_type and emp_type != 'All':
        jobs_qs = jobs_qs.filter(employment_type=emp_type)

    # 7. Salary Filtering
    min_sal = request.GET.get('min_salary', '').strip()
    if min_sal:
        try:
            jobs_qs = jobs_qs.filter(salary_avg__gte=float(min_sal))
        except ValueError:
            pass

    max_sal = request.GET.get('max_salary', '').strip()
    if max_sal:
        try:
            jobs_qs = jobs_qs.filter(salary_avg__lte=float(max_sal))
        except ValueError:
            pass

    # 8. Sorting
    sort = request.GET.get('sort', 'recent')
    if sort == 'salary_high':
        jobs_qs = jobs_qs.order_by('-salary_avg')
    elif sort == 'salary_low':
        jobs_qs = jobs_qs.order_by('salary_avg')
    elif sort == 'title':
        jobs_qs = jobs_qs.order_by('title')
    else:
        jobs_qs = jobs_qs.order_by('-posted_date', '-id')

    total_count = jobs_qs.count()

    # Pagination: 12 jobs per page
    paginator = Paginator(jobs_qs, 12)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Get Filter Options for Sidebar
    all_roles = Job.objects.values_list('role_category', flat=True).distinct().order_by('role_category')
    all_locations = ['Bengaluru', 'Mumbai', 'Pune', 'Hyderabad', 'Delhi-NCR', 'Gurugram', 'Noida', 'Chennai', 'Remote']
    all_experiences = ['Entry Level', 'Mid Level', 'Senior Level', 'Lead / Principal']
    all_work_modes = ['Remote', 'Hybrid', 'On-site']
    all_emp_types = ['Full Time', 'Contract', 'Internship', 'Part Time']

    # Saved jobs ids for current user
    saved_job_ids = set()
    if request.user.is_authenticated:
        saved_job_ids = set(SavedJob.objects.filter(user=request.user).values_list('job_id', flat=True))

    context = {
        'jobs': page_obj,
        'total_count': total_count,
        'form': form,
        'all_roles': all_roles,
        'all_locations': all_locations,
        'all_experiences': all_experiences,
        'all_work_modes': all_work_modes,
        'all_emp_types': all_emp_types,
        'selected_q': q,
        'selected_role': role,
        'selected_location': location,
        'selected_experience': experience,
        'selected_work_mode': work_mode,
        'selected_emp_type': emp_type,
        'selected_min_salary': min_sal,
        'selected_max_salary': max_sal,
        'selected_sort': sort,
        'saved_job_ids': saved_job_ids,
    }
    return render(request, 'jobs/job_list.html', context)


def job_detail(request, pk):
    job = get_object_or_404(Job.objects.select_related('company').prefetch_related('skills'), pk=pk)
    
    # Increment view counter
    Job.objects.filter(pk=pk).update(views_count=job.views_count + 1)

    # Similar jobs
    similar_jobs = Job.objects.filter(
        role_category=job.role_category
    ).exclude(pk=job.pk).select_related('company').prefetch_related('skills')[:4]

    is_saved = False
    if request.user.is_authenticated:
        is_saved = SavedJob.objects.filter(user=request.user, job=job).exists()

    context = {
        'job': job,
        'similar_jobs': similar_jobs,
        'is_saved': is_saved,
    }
    return render(request, 'jobs/job_detail.html', context)


@login_required
def toggle_save_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    saved_obj, created = SavedJob.objects.get_or_create(user=request.user, job=job)
    
    if not created:
        saved_obj.delete()
        is_saved = False
        msg = f"Removed '{job.title}' from saved jobs."
    else:
        is_saved = True
        msg = f"Saved '{job.title}' to your profile."

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('format') == 'json':
        return JsonResponse({'status': 'success', 'is_saved': is_saved, 'message': msg})
    
    messages.success(request, msg)
    return redirect(request.META.get('HTTP_REFERER', 'jobs:job_detail', pk=pk))


@login_required
def saved_jobs(request):
    saved_list = SavedJob.objects.filter(user=request.user).select_related('job', 'job__company').prefetch_related('job__skills')
    return render(request, 'jobs/saved_jobs.html', {'saved_jobs': saved_list})
