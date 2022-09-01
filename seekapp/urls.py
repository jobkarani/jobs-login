from http import server
from unicodedata import name
from django import urls
from django.urls import URLPattern, URLResolver, path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views as app_views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/options/', views.options, name='options'),
    path('jobseeker/profile/', views.profile_jobseeker, name='profile_jobseeker'),
    path('jobseeker/profile/<int:id>',
         views.jobseeker_profile, name='jobseeker_profile'),
    path('update_jobseeker_profile/', views.update_jobseeker_profile,
         name='update_jobseeker_profile'),
    path('employer/profile/', views.employerProfile, name='profile'),
    path('update_employer_profile/',
         views.update_employer_profile, name='update_employer'),
    path('signup/jobseeker/', views.jobseeker_signup, name='jobseeker_signup'),
    path('signup/employer/', views.employer_signup, name='employer_signup'),
]
