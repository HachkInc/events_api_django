from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Events, Tickets

# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'name', 'surname', 'age', 'email','is_staff' , 'is_admin', 'password',)


class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ('id', 'title', 'login', 'password', 'address', 'time_start', 'time_end', 'max_guest_count',
                  'description')


class TicketsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tickets
        fields = ('id', 'event_id', 'is_inside')
