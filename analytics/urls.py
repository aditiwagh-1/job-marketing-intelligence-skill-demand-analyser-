from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('skills/', views.skill_demand, name='skill_demand'),
    path('salary/', views.salary_intelligence, name='salary_intelligence'),
    path('locations/', views.location_insights, name='location_insights'),
    path('api/skills/', views.api_skill_demand, name='api_skill_demand'),
]
