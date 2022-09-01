from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction
from .models import *


class JobseekerSignUp(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'email', 'password1', 'password2']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_jobseeker = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()
        jobseeker = JobSeeker.objects.create(user=user)
        jobseeker.email = self.cleaned_data.get('email')
        jobseeker.save()

        return jobseeker


class EmployerSignUp(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'email', 'password1', 'password2']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_employer = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()
        employer = Employer.objects.create(user=user)
        employer.email = self.cleaned_data.get('email')

        employer.save()

        return employer



class UpdateJobseekerProfile(forms.ModelForm):

    class Meta:
        model = JobSeeker
        fields = ( 'salary',
                  'location','contact', 'bio', 'profile_photo')


        # widgets = {
        #     'contact': forms.CharField(attrs={'class': 'col-md-6'})
        # }

class UpdateUserProfile(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class UpdateEmployerProfile(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ('company', 'profile_photo', )
