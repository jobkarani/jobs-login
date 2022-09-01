import json
from urllib.request import HTTPBasicAuthHandler
from django.shortcuts import render, redirect
from seekapp.models import *
from django.contrib.auth.decorators import login_required
from .forms import *
from django.shortcuts import redirect, render, get_object_or_404
from seekapp.models import *
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
import os
import time
from .email import *
from django.http.response import Http404
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from os import access
from decouple import config, Csv
from django.views.decorators.csrf import csrf_exempt
import json
import requests



def options(request):
    return render(request, 'registration/options.html')


def home(request):
    return render(request, 'index.html')


@login_required
def jobseeker_profile(request, id):
    jobseeker = User.objects.get(id=id)
    profile = JobSeeker.objects.get(user_id=id)  # get profile
    # user = get_object_or_404(User, pk=user.id)
    return render(request, "employer/jobseekerview.html", {"jobseeker": jobseeker, "profile": profile})
# jobseekers update profile


@login_required
def profile_jobseeker(request):
    current_user = request.user
    user = get_object_or_404(User, pk=current_user.id)
    profile = JobSeeker.objects.get(user_id=current_user.id)  # get profile
    return render(request, "jobseeker/profile.html", { "current_user": current_user, "profile": profile})


@login_required
def update_jobseeker_profile(request):
    current_user = request.user
    profile = JobSeeker.objects.get(user_id=current_user.id)
    if request.method == 'POST':
        user_form = UpdateUserProfile(
            request.POST, request.FILES, instance=request.user)
        jobseeker_form = UpdateJobseekerProfile(
            request.POST, request.FILES, instance=request.user.jobseeker)
        if user_form.is_valid() and jobseeker_form.is_valid():
            user_form.save()
            jobseeker_form.save()
            messages.success(
                request, 'Your Profile account has been updated successfully')
            return redirect('profile_jobseeker')
    else:
        user_form = UpdateUserProfile(instance=request.user)
        jobseeker_form = UpdateJobseekerProfile(
            instance=request.user.jobseeker)
    params = {
        'user_form': user_form,
        'jobseeker_form': jobseeker_form,
        'profile': profile
    }
    return render(request, 'jobseeker/update.html', params)

@login_required
def delete_jobseeker(request, user_id):
    jobseeker = JobSeeker.objects.get(pk=user_id)
    if jobseeker:
        jobseeker.delete_user()
        messages.success(request, f'User deleted successfully!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# employer profle


@login_required
def employerProfile(request):
    employer = request.user
    profile = Employer.objects.get(user_id=employer.id)  # get profile
    available = User.objects.filter(is_jobseeker=True).all()
    profile = Employer.objects.filter(
        user_id=employer.id).first()  # get profile
    context = {
        "employer": employer,
        "available": available,
        'profile': profile
    }
    return render(request, 'employer/profile.html', context)


@login_required
def update_employer_profile(request):
    current_user = request.user
    profile = Employer.objects.get(
        user_id=current_user.id)  # get profile
    if request.method == 'POST':
        u_form = UpdateUserProfile(
            request.POST, request.FILES, instance=request.user)
        p_form = UpdateEmployerProfile(
            request.POST, request.FILES, instance=request.user.employer)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(
                request, 'Your Profile account has been updated successfully')
            return redirect('profile')
    else:
        u_form = UpdateUserProfile(instance=request.user)
        p_form = UpdateEmployerProfile(instance=request.user.employer)
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'profile': profile
    }
    return render(request, 'employer/update.html', context)


def emp_home(request):
    return render(request, 'employer/home.html')


def jobseeker_home(request):
    return render(request, 'jobseeker/home.html')


def jobseeker_signup(request):
    # if request.user.is_authenticated:
    #     return redirect('home')
    if request.method == "POST":
        form = JobseekerSignUp(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            return redirect('login')

    else:
        form = JobseekerSignUp()
    return render(request, "registration/register.html", {'form': form})


def employer_signup(request):
    # if request.user.is_authenticated:
    #     return redirect('home')
    if request.method == "POST":
        form = EmployerSignUp(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            return redirect('login')

    else:
        form = EmployerSignUp()
    return render(request, "registration/register.html", {'form': form})

