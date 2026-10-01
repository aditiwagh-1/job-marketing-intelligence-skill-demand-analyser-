from django.contrib import admin
from .models import Skill, Company, Job, SavedJob


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'importance_weight')
    list_filter = ('category',)
    search_fields = ('name', 'description')


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'industry', 'location', 'company_size', 'rating')
    list_filter = ('industry', 'location')
    search_fields = ('name', 'description')


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'role_category', 'location', 'experience_level', 'salary_avg', 'work_mode', 'posted_date')
    list_filter = ('role_category', 'experience_level', 'work_mode', 'location', 'company__industry')
    search_fields = ('title', 'company__name', 'description')
    filter_horizontal = ('skills',)


@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'saved_at')
    list_filter = ('saved_at',)
    search_fields = ('user__username', 'job__title')
