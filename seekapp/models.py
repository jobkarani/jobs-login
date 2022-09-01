from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
from tinymce.models import HTMLField
from django.contrib.auth.models import PermissionsMixin
from django.db import models
# Create your models here.


class User(AbstractUser):
    USERNAME_FIELD = 'username'
    is_admin = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False)
    is_jobseeker = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def save_user(self):
        self.save()

    def update_user(self):
        self.update()

    def delete_user(self):
        self.delete()


class JobSeeker(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    # firstName = models.CharField(max_length=100, null=True, blank=True)
    # lastName = models.CharField(max_length=100, null=True, blank=True)
    profile_photo = CloudinaryField('image', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    contact = models.CharField(
        unique=True, max_length=30, null=True, blank=True)
    salary = models.IntegerField(null=True, blank=True)
    email = models.CharField(max_length=50, null=True)

    def save_jobseeker(self):
        self.save()

    def delete_jobseeker(self):
        self.delete()

    @classmethod
    def update_jobseeker(self):
        self.update()

    @classmethod
    def search_jobseekers_by_job_category(cls, job_category):
        jobseekers = JobSeeker.objects.filter(
            job_category__icontains=job_category)
        return jobseekers

    # def __str__(self):
    #     return self.username


class Employer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    # firstName = models.CharField(max_length=100, null=True, blank=True)
    # lastName = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=50, null=True)
    profile_photo = CloudinaryField('image', null=True, blank=True)
    company = models.CharField(max_length=100, null=True, blank=True)

    def save_employer(self):
        self.save()

    def update_employer(self):
        self.update()

    def delete_employer(self):
        self.delete()
