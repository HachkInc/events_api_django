from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, AbstractUser

)


class User(AbstractUser):
    id = models.CharField(max_length=6, primary_key=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    age = models.CharField(max_length=3, blank=True)
    is_superuser = models.BooleanField(blank=True)
    is_staff = models.BooleanField(blank=True)
    email = models.EmailField()
    password = models.CharField(max_length=150)


class Events(models.Model):
    id = models.CharField(max_length=6, primary_key=True)
    title = models.CharField(max_length=150)
    login = models.CharField(max_length=20)
    password = models.CharField(max_length=40)
    address = models.CharField(max_length=150)
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
    max_guest_count = models.IntegerField()
    description = models.CharField(max_length=1000)


class Tickets(models.Model):
    id = models.CharField(max_length=6, primary_key=True)
    # id = models.SlugField(primary_key=True, unique=True, editable=False, blank=True)
    event_id = models.ForeignKey(Events, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, default="", on_delete=models.CASCADE)
    is_inside = models.BooleanField()
