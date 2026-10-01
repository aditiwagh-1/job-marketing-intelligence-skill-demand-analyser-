from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .forms import UserRegisterForm, UserLoginForm, UserProfileForm
from .models import UserProfile, UserSkill
from jobs.models import Skill, SavedJob, Job
from recommendations.services import calculate_skill_gap, get_career_recommendations


def user_register(request):
    if request.user.is_authenticated:
        return redirect('accounts:profile')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Profile is automatically created by signal, let's attach default skills
            profile = user.profile
            default_skills = Skill.objects.filter(name__in=['SQL', 'Python', 'Excel'])
            for s in default_skills:
                UserSkill.objects.create(user_profile=profile, skill=s, proficiency='Intermediate')

            login(request, user)
            messages.success(request, f'Welcome to Job Market Intelligence, {user.username}! Your career profile has been created.')
            return redirect('accounts:profile')
    else:
        form = UserRegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('accounts:profile')

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                next_url = request.GET.get('next') or 'accounts:profile'
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.info(request, 'You have been successfully logged out.')
    return redirect('core:home')


@login_required
def profile(request):
    profile_obj = request.user.profile
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile_obj)
        if form.is_valid():
            form.save()
            
            # Handle selected skills
            selected_skill_ids = request.POST.getlist('profile_skills')
            if selected_skill_ids:
                UserSkill.objects.filter(user_profile=profile_obj).delete()
                for sid in selected_skill_ids:
                    try:
                        skill = Skill.objects.get(id=sid)
                        UserSkill.objects.create(user_profile=profile_obj, skill=skill, proficiency='Intermediate')
                    except Skill.DoesNotExist:
                        pass

            messages.success(request, 'Your profile and skill set have been updated successfully!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=profile_obj)

    user_skills = profile_obj.profile_skills.select_related('skill').all()
    user_skill_names = [us.skill.name for us in user_skills]
    user_skill_ids = set([us.skill.id for us in user_skills])
    all_skills = Skill.objects.all().order_by('category', 'name')
    saved_jobs = SavedJob.objects.filter(user=request.user).select_related('job', 'job__company')

    # Instant intelligence metrics for user
    target_role = profile_obj.target_role or 'Data Analyst'
    gap_summary = calculate_skill_gap(user_skill_names, target_role)
    career_matches = get_career_recommendations(user_skill_names)[:4]

    context = {
        'form': form,
        'profile': profile_obj,
        'user_skills': user_skills,
        'user_skill_ids': user_skill_ids,
        'all_skills': all_skills,
        'saved_jobs': saved_jobs,
        'gap_summary': gap_summary,
        'career_matches': career_matches,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def update_profile_skills_ajax(request):
    if request.method == 'POST':
        profile_obj = request.user.profile
        skill_id = request.POST.get('skill_id')
        action = request.POST.get('action') # 'add' or 'remove'

        try:
            skill = Skill.objects.get(id=skill_id)
            if action == 'add':
                UserSkill.objects.get_or_create(user_profile=profile_obj, skill=skill)
                status = 'added'
            elif action == 'remove':
                UserSkill.objects.filter(user_profile=profile_obj, skill=skill).delete()
                status = 'removed'
            else:
                status = 'noop'

            current_skills = list(profile_obj.skills.values_list('name', flat=True))
            return JsonResponse({'status': 'success', 'action': status, 'skills': current_skills})
        except Skill.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Skill not found'}, status=404)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
