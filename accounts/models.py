from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from jobs.models import Skill


class UserProfile(models.Model):
    EDUCATION_CHOICES = [
        ("Bachelor's Degree", "Bachelor's Degree (B.Tech / BCA / B.Sc / BE)"),
        ("Master's Degree", "Master's Degree (M.Tech / MCA / M.Sc / MS)"),
        ("MBA", "Master of Business Administration (MBA)"),
        ("Doctorate / PhD", "Doctorate / PhD"),
        ("Diploma / Associate", "Diploma / Associate Degree"),
        ("Self-Taught / Bootcamp", "Self-Taught / Bootcamp Graduate"),
    ]

    WORK_PREFERENCE_CHOICES = [
        ('Any', 'Any Work Mode'),
        ('Remote', 'Remote Only'),
        ('Hybrid', 'Hybrid Preferred'),
        ('On-site', 'On-site Preferred'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    headline = models.CharField(max_length=200, blank=True, default='Data & Tech Professional')
    target_role = models.CharField(max_length=100, default='Data Analyst')
    education = models.CharField(max_length=100, choices=EDUCATION_CHOICES, default="Bachelor's Degree")
    years_of_experience = models.FloatField(default=1.0)
    current_salary = models.FloatField(blank=True, null=True, help_text='Current CTC in LPA')
    expected_salary = models.FloatField(blank=True, null=True, help_text='Expected CTC in LPA')
    preferred_location = models.CharField(max_length=100, default='Bengaluru')
    preferred_work_mode = models.CharField(max_length=50, choices=WORK_PREFERENCE_CHOICES, default='Any')
    bio = models.TextField(blank=True, default='Passionate about data-driven decision making and solving complex problems.')
    github_url = models.URLField(max_length=200, blank=True, null=True)
    linkedin_url = models.URLField(max_length=200, blank=True, null=True)
    skills = models.ManyToManyField(Skill, through='UserSkill', related_name='user_profiles', blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def get_skill_names(self):
        return list(self.skills.values_list('name', flat=True))


class UserSkill(models.Model):
    PROFICIENCY_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
        ('Expert', 'Expert'),
    ]

    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='profile_skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='user_skills')
    proficiency = models.CharField(max_length=50, choices=PROFICIENCY_CHOICES, default='Intermediate')
    years_practiced = models.FloatField(default=1.0)

    class Meta:
        unique_together = ('user_profile', 'skill')
        ordering = ['skill__name']

    def __str__(self):
        return f"{self.user_profile.user.username} - {self.skill.name} ({self.proficiency})"


@receiver(post_save, sender=User)
def create_or_save_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()
