from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('<int:pk>/', views.job_detail, name='job_detail'),
    path('<int:pk>/save/', views.toggle_save_job, name='toggle_save_job'),
    path('saved/', views.saved_jobs, name='saved_jobs'),
]
