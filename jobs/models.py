from django.db import models
from django.contrib.auth.models import User


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('programming', 'Programming Languages'),
        ('database', 'Databases & Warehousing'),
        ('visualization', 'Visualization & BI'),
        ('analytics', 'Analytics & Statistics'),
        ('cloud_devops', 'Cloud & DevOps'),
        ('ai_ml', 'AI & Machine Learning'),
        ('web_mobile', 'Web & Frameworks'),
        ('tools_other', 'Tools & Methodologies'),
    ]

    name = models.CharField(max_length=100, unique=True, db_index=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='programming', db_index=True)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=50, blank=True, default='fa-solid fa-code')
    importance_weight = models.FloatField(default=1.0)

    class Meta:
        ordering = ['name']
        verbose_name = 'Skill'
        verbose_name_plural = 'Skills'

    def __str__(self):
        return self.name


class Company(models.Model):
    INDUSTRY_CHOICES = [
        ('FinTech', 'Financial Technology & Banking'),
        ('SaaS', 'Enterprise SaaS & Cloud Software'),
        ('E-Commerce', 'E-Commerce & Retail Tech'),
        ('AI_Cloud', 'AI & Cloud Infrastructure'),
        ('EdTech', 'Education Technology'),
        ('HealthTech', 'Healthcare & Life Sciences'),
        ('Consulting', 'IT Services & Consulting'),
        ('Logistics', 'Supply Chain & Logistics Tech'),
        ('Cybersecurity', 'Cybersecurity & InfoSec'),
    ]

    name = models.CharField(max_length=150, unique=True, db_index=True)
    website = models.URLField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=100, default='Bengaluru, India')
    industry = models.CharField(max_length=50, choices=INDUSTRY_CHOICES, default='SaaS', db_index=True)
    company_size = models.CharField(max_length=50, default='500-1000 employees')
    logo_color = models.CharField(max_length=20, default='indigo')
    description = models.TextField(blank=True, null=True)
    rating = models.FloatField(default=4.2)

    class Meta:
        ordering = ['name']
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.name


class Job(models.Model):
    ROLE_CHOICES = [
        ('Data Analyst', 'Data Analyst'),
        ('Data Scientist', 'Data Scientist'),
        ('Business Intelligence Analyst', 'Business Intelligence Analyst'),
        ('Machine Learning Engineer', 'Machine Learning Engineer'),
        ('Data Engineer', 'Data Engineer'),
        ('Full Stack Developer', 'Full Stack Developer'),
        ('Frontend Developer', 'Frontend Developer'),
        ('Backend Developer', 'Backend Developer'),
        ('DevOps Engineer', 'DevOps Engineer'),
        ('Cloud Architect', 'Cloud Architect'),
        ('Cybersecurity Analyst', 'Cybersecurity Analyst'),
        ('Product Manager', 'Product Manager'),
        ('AI Research Engineer', 'AI Research Engineer'),
        ('Database Administrator', 'Database Administrator'),
        ('QA Automation Engineer', 'QA Automation Engineer'),
    ]

    EXPERIENCE_CHOICES = [
        ('Entry Level', 'Entry Level (0-2 years)'),
        ('Mid Level', 'Mid Level (3-5 years)'),
        ('Senior Level', 'Senior Level (6-9 years)'),
        ('Lead / Principal', 'Lead / Principal (10+ years)'),
    ]

    EMPLOYMENT_CHOICES = [
        ('Full Time', 'Full Time'),
        ('Part Time', 'Part Time'),
        ('Contract', 'Contract'),
        ('Internship', 'Internship'),
    ]

    WORK_MODE_CHOICES = [
        ('Remote', 'Remote'),
        ('Hybrid', 'Hybrid'),
        ('On-site', 'On-site'),
    ]

    title = models.CharField(max_length=200, db_index=True)
    role_category = models.CharField(max_length=100, choices=ROLE_CHOICES, db_index=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')
    location = models.CharField(max_length=100, db_index=True)
    experience_level = models.CharField(max_length=50, choices=EXPERIENCE_CHOICES, db_index=True)
    experience_min = models.IntegerField(default=0)
    experience_max = models.IntegerField(default=2)
    employment_type = models.CharField(max_length=50, choices=EMPLOYMENT_CHOICES, default='Full Time')
    work_mode = models.CharField(max_length=50, choices=WORK_MODE_CHOICES, default='Hybrid', db_index=True)
    
    # Salary in LPA (Lakhs Per Annum in INR)
    salary_min = models.FloatField(help_text='Minimum Salary in LPA')
    salary_max = models.FloatField(help_text='Maximum Salary in LPA')
    salary_avg = models.FloatField(help_text='Average Salary in LPA', db_index=True)

    description = models.TextField()
    responsibilities = models.TextField(blank=True, null=True)
    requirements = models.TextField(blank=True, null=True)
    benefits = models.TextField(blank=True, null=True)

    skills = models.ManyToManyField(Skill, related_name='jobs', blank=True)
    posted_date = models.DateField(db_index=True)
    is_active = models.BooleanField(default=True)
    views_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-posted_date', '-id']
        indexes = [
            models.Index(fields=['role_category', 'location']),
            models.Index(fields=['salary_avg', 'experience_level']),
        ]
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'

    def __str__(self):
        return f"{self.title} at {self.company.name}"

    def save(self, *args, **kwargs):
        if not self.salary_avg:
            self.salary_avg = round((self.salary_min + self.salary_max) / 2.0, 2)
        super().save(*args, **kwargs)


class SavedJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_jobs')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='saved_by_users')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')
        ordering = ['-saved_at']

    def __str__(self):
        return f"{self.user.username} saved {self.job.title}"
