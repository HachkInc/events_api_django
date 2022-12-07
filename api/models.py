import django_filters
from django.db import models
from django_filters import rest_framework as filters
from django.db.models import Q


# from django_filters import filters
# class User(models.Model):
#     id_Pk = models.IntegerField()
#     name = models.CharField(max_length=20)
#     surname = models.CharField(max_length=20)
#     age = models.IntegerField()
#     email = models.CharField(max_length=50)
#     # qr_code = models.CharField(max_length=50)
#     is_staff = models.BooleanField()
#     is_admin = models.BooleanField()
#     password = models.CharField(max_length=20)
#
#     def __str__(self):
#         return self.name + ' ' + self.surname


class Events(models.Model):
    # id = models.AutoField(primary_key = True)
    title = models.CharField(max_length=40)
    login = models.CharField(max_length=20)
    password = models.CharField(max_length=40)
    address = models.CharField(max_length=100)
    # qr_code = models.CharField(max_length=50)
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
    max_guest_count = models.IntegerField()
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Tickets(models.Model):
    event_id = models.ForeignKey(Events, on_delete=models.CASCADE)
    # event_id = models.IntegerField()
    # client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    is_inside = models.BooleanField()
