import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'job_market.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from jobs.models import Job, Company, Skill, SavedJob
from recommendations.ml_engine import predict_salary

def run_verification():
    print("=" * 60)
    print("RUNNING COMPREHENSIVE AUTOMATED VERIFICATION SUITE")
    print("=" * 60)
    
    client = Client()
    
    # 1. Test Core Views
    print("\n[1/7] Testing Core Views...")
    r = client.get('/')
    assert r.status_code == 200, f"Home page failed: {r.status_code}"
    assert b"JOB MARKET" in r.content, "Home page content missing"
    assert b"LIVE DATA" in r.content
    print("  [PASS] Home Landing Page (/) -> HTTP 200 OK")

    r = client.get('/about/')
    assert r.status_code == 200, f"About page failed: {r.status_code}"
    assert b"Modular 5-App Django Architecture" in r.content
    print("  [PASS] About Page (/about/) -> HTTP 200 OK")

    # 2. Test Analytics Views
    print("\n[2/7] Testing Analytics Views & Charts Data...")
    r = client.get('/analytics/dashboard/')
    assert r.status_code == 200, f"Dashboard failed: {r.status_code}"
    assert b"chart-roles" in r.content
    assert b"chart-skills" in r.content
    print("  [PASS] Market Dashboard (/analytics/dashboard/) -> HTTP 200 OK")

    r = client.get('/analytics/skills/?role=Data+Analyst')
    assert r.status_code == 200, f"Skill demand failed: {r.status_code}"
    assert b"chart-radar" in r.content
    print("  [PASS] Skill Demand Analytics (/analytics/skills/?role=Data+Analyst) -> HTTP 200 OK")

    r = client.get('/analytics/salary/?role=Data+Scientist&location=Bengaluru')
    assert r.status_code == 200, f"Salary intelligence failed: {r.status_code}"
    assert b"chart-salary-dist" in r.content
    assert b"chart-exp-salary" in r.content
    print("  [PASS] Salary Intelligence (/analytics/salary/) -> HTTP 200 OK")

    r = client.get('/analytics/locations/')
    assert r.status_code == 200, f"Location insights failed: {r.status_code}"
    assert b"chart-locations-volume" in r.content
    print("  [PASS] Location Insights (/analytics/locations/) -> HTTP 200 OK")

    # 3. Test Jobs Views
    print("\n[3/7] Testing Jobs Search & Filtering...")
    r = client.get('/jobs/')
    assert r.status_code == 200, f"Jobs list failed: {r.status_code}"
    assert b"Search Tech Jobs" in r.content
    print("  [PASS] Jobs Listing Page (/jobs/) -> HTTP 200 OK")

    first_job = Job.objects.first()
    assert first_job is not None, "No jobs in database"
    r = client.get(f'/jobs/{first_job.id}/')
    assert r.status_code == 200, f"Job detail failed: {r.status_code}"
    assert first_job.title.encode() in r.content
    print(f"  [PASS] Job Detail Page (/jobs/{first_job.id}/) -> HTTP 200 OK")

    # 4. Test Recommendations & Skill Gap
    print("\n[4/7] Testing Recommendations Engine...")
    r = client.get('/recommendations/skill-gap/?target_role=Data+Scientist&skills=Python&skills=SQL&skills=Excel')
    assert r.status_code == 200, f"Skill gap failed: {r.status_code}"
    assert b"Skill Gap Analyzer" in r.content
    assert b"Recommended Learning Roadmap" in r.content
    print("  [PASS] Skill Gap Analyzer (/recommendations/skill-gap/) -> HTTP 200 OK")

    r = client.get('/recommendations/careers/')
    assert r.status_code == 200, f"Career recommendations failed: {r.status_code}"
    assert b"Recommended Career Paths" in r.content
    print("  [PASS] Career Recommendations (/recommendations/careers/) -> HTTP 200 OK")

    r = client.get('/recommendations/jobs/')
    assert r.status_code == 200, f"Job recommendations failed: {r.status_code}"
    assert b"Recommended Jobs for Your Skill Set" in r.content
    print("  [PASS] Job Recommendations (/recommendations/jobs/) -> HTTP 200 OK")

    # 5. Test ML Salary Predictor
    print("\n[5/7] Testing ML Salary Predictor...")
    r = client.post('/recommendations/salary-predictor/', {
        'role': 'Machine Learning Engineer',
        'experience_years': '4.5',
        'location': 'Bengaluru',
        'education': "Master's Degree",
        'work_mode': 'Hybrid',
        'skills': ['Python', 'Machine Learning', 'PyTorch', 'Docker']
    })
    assert r.status_code == 200, f"Salary predictor failed: {r.status_code}"
    assert b"Predicted Annual CTC" in r.content
    assert b"Estimated Monthly In-Hand" in r.content
    print("  [PASS] ML Salary Predictor (/recommendations/salary-predictor/) -> HTTP 200 OK")

    # 6. Test User Authentication & Profile
    print("\n[6/7] Testing Accounts, Login & Profile Flow...")
    r = client.get('/accounts/login/')
    assert r.status_code == 200
    print("  [PASS] Login Page (/accounts/login/) -> HTTP 200 OK")

    r = client.get('/accounts/register/')
    assert r.status_code == 200
    print("  [PASS] Register Page (/accounts/register/) -> HTTP 200 OK")

    login_success = client.login(username='demo_user', password='demopassword123')
    assert login_success, "Failed to login with demo credentials"
    print("  [PASS] Authentication of demo_user -> SUCCESS")

    r = client.get('/accounts/profile/')
    assert r.status_code == 200
    assert b"My Technical Skills" in r.content
    print("  [PASS] Authenticated Profile Dashboard (/accounts/profile/) -> HTTP 200 OK")

    r = client.get('/jobs/saved/')
    assert r.status_code == 200
    assert b"Saved Jobs" in r.content
    print("  [PASS] Saved Jobs Page (/jobs/saved/) -> HTTP 200 OK")

    # 7. Test Bookmark Toggle
    print("\n[7/7] Testing Job Bookmarking Action...")
    r = client.post(f'/jobs/{first_job.id}/save/?format=json', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    assert r.status_code == 200
    json_res = r.json()
    assert json_res['status'] == 'success'
    print(f"  [PASS] AJAX Job Bookmark Toggle -> SUCCESS ({json_res['message']})")

    print("\n" + "=" * 60)
    print("ALL 7 VERIFICATION MODULES PASSED WITH 100% SUCCESS!")
    print("=" * 60)

if __name__ == '__main__':
    run_verification()
