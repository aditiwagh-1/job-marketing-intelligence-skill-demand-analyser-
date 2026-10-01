from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, UserSkill
from jobs.models import Skill


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Choose a secure password',
        'class': 'w-full bg-slate-900/80 border border-slate-700 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 text-sm'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm your password',
        'class': 'w-full bg-slate-900/80 border border-slate-700 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 text-sm'
    }))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Choose a username', 'class': 'w-full bg-slate-900/80 border border-slate-700 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 text-sm'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First name', 'class': 'w-full bg-slate-900/80 border border-slate-700 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 text-sm'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last name', 'class': 'w-full bg-slate-900/80 border border-slate-700 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 text-sm'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email address', 'class': 'w-full bg-slate-900/80 border border-slate-700 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 text-sm'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Username or Email',
        'class': 'w-full bg-slate-900/80 border border-slate-700 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 text-sm'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class': 'w-full bg-slate-900/80 border border-slate-700 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 text-sm'
    }))


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'headline', 'target_role', 'education', 'years_of_experience',
            'current_salary', 'expected_salary', 'preferred_location',
            'preferred_work_mode', 'bio', 'github_url', 'linkedin_url'
        ]
        widgets = {
            'headline': forms.TextInput(attrs={'class': 'w-full bg-slate-900/80 border border-slate-700 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-indigo-500 text-sm'}),
            'target_role': forms.TextInput(attrs={'class': 'w-full bg-slate-900/80 border border-slate-700 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-indigo-500 text-sm'}),
            'education': forms.Select(attrs={'class': 'w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-indigo-500 text-sm'}),
            'years_of_experience': forms.NumberInput(attrs={'step': '0.5', 'class': 'w-full bg-slate-900/80 border border-slate-700 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-indigo-500 text-sm'}),
            'current_salary': forms.NumberInput(attrs={'step': '0.1', 'placeholder': 'e.g. 6.5', 'class': 'w-full bg-slate-900/80 border border-slate-700 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-indigo-500 text-sm'}),
            'expected_salary': forms.NumberInput(attrs={'step': '0.1', 'placeholder': 'e.g. 10.0', 'class': 'w-full bg-slate-900/80 border border-slate-700 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-indigo-500 text-sm'}),
            'preferred_location': forms.TextInput(attrs={'class': 'w-full bg-slate-900/80 border border-slate-700 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-indigo-500 text-sm'}),
            'preferred_work_mode': forms.Select(attrs={'class': 'w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-indigo-500 text-sm'}),
            'bio': forms.Textarea(attrs={'rows': 3, 'class': 'w-full bg-slate-900/80 border border-slate-700 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-indigo-500 text-sm'}),
            'github_url': forms.URLInput(attrs={'placeholder': 'https://github.com/username', 'class': 'w-full bg-slate-900/80 border border-slate-700 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-indigo-500 text-sm'}),
            'linkedin_url': forms.URLInput(attrs={'placeholder': 'https://linkedin.com/in/username', 'class': 'w-full bg-slate-900/80 border border-slate-700 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-indigo-500 text-sm'}),
        }
