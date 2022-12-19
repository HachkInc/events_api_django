from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, User

)

class Events(models.Model):
    title = models.CharField(max_length=150)
    login = models.CharField(max_length=20)
    password = models.CharField(max_length=40)
    address = models.CharField(max_length=150)
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
    max_guest_count = models.IntegerField()
    description = models.CharField(max_length=1000)


class Tickets(models.Model):
    event_id = models.ForeignKey(Events, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, default = "" ,on_delete=models.CASCADE)
    is_inside = models.BooleanField()
