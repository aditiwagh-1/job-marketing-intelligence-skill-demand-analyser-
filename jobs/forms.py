from django import forms
from .models import Job


class JobFilterForm(forms.Form):
    q = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Search job title, skills, company...',
        'class': 'w-full bg-slate-900/80 border border-slate-700 rounded-xl px-4 py-2.5 text-white placeholder-slate-400 focus:outline-none focus:border-indigo-500 text-sm'
    }))
    
    role = forms.CharField(required=False)
    location = forms.CharField(required=False)
    experience = forms.CharField(required=False)
    work_mode = forms.CharField(required=False)
    employment_type = forms.CharField(required=False)
    min_salary = forms.FloatField(required=False)
    max_salary = forms.FloatField(required=False)
    sort = forms.CharField(required=False, initial='recent')
