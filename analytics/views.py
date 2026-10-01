import json
from django.shortcuts import render
from django.http import JsonResponse
from .services import (
    get_kpi_summary,
    get_dashboard_charts_data,
    get_skill_demand_analytics,
    get_salary_intelligence_data,
    get_location_insights_data,
)


def dashboard(request):
    kpis = get_kpi_summary()
    charts_data = get_dashboard_charts_data()
    
    context = {
        'kpis': kpis,
        'charts_data_json': json.dumps(charts_data),
    }
    return render(request, 'analytics/dashboard.html', context)


def skill_demand(request):
    selected_role = request.GET.get('role', 'All Roles')
    analytics_data = get_skill_demand_analytics(selected_role)
    
    context = {
        'data': analytics_data,
        'radar_json': json.dumps(analytics_data['category_radar']),
        'top_skills_json': json.dumps([
            {'name': s['name'], 'pct': s['percentage']} for s in analytics_data['top_skills']
        ]),
    }
    return render(request, 'analytics/skill_demand.html', context)


def salary_intelligence(request):
    role = request.GET.get('role', 'All')
    location = request.GET.get('location', 'All')
    experience = request.GET.get('experience', 'All')

    data = get_salary_intelligence_data(role, location, experience)

    context = {
        'data': data,
        'dist_json': json.dumps(data['distribution']),
        'exp_salary_json': json.dumps(data['experience_salary']),
        'loc_salary_json': json.dumps(data['location_salary']),
    }
    return render(request, 'analytics/salary_intelligence.html', context)


def location_insights(request):
    data = get_location_insights_data()
    context = {
        'locations': data['locations'],
        'chart_json': json.dumps(data['top_locations_chart']),
    }
    return render(request, 'analytics/location_insights.html', context)


def api_skill_demand(request):
    role = request.GET.get('role', 'All Roles')
    data = get_skill_demand_analytics(role)
    return JsonResponse(data)
