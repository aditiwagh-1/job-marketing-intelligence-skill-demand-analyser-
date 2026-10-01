from django.contrib import admin
from .models import UserProfile, UserSkill


class UserSkillInline(admin.TabularInline):
    model = UserSkill
    extra = 1


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'target_role', 'years_of_experience', 'preferred_location', 'education')
    search_fields = ('user__username', 'user__email', 'target_role')
    inlines = [UserSkillInline]


@admin.register(UserSkill)
class UserSkillAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'skill', 'proficiency', 'years_practiced')
    list_filter = ('proficiency', 'skill__category')
