from django.urls import path
from . import views

app_name = 'recommendations'

urlpatterns = [
    path('skill-gap/', views.skill_gap, name='skill_gap'),
    path('careers/', views.career_recommendations, name='career_recommendations'),
    path('jobs/', views.job_recommendations, name='job_recommendations'),
    path('salary-predictor/', views.salary_predictor, name='salary_predictor'),
]
