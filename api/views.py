from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from django_filters import rest_framework as filters
from .serializers import EventsSerializer, TicketsSerializer
from .models import Events, Tickets
from django.contrib.auth import authenticate, login

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, RegisterSerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from django.contrib.auth.models import User
# from snippets.serializers import UserSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Class based view to register user
class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class EventFilterSet(filters.FilterSet):
    class Meta:
        model = Events
        fields = {
            'title': ['icontains'],
        }


class EventsViewSet(viewsets.ModelViewSet):
    queryset = Events.objects.all()
    serializer_class = EventsSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EventFilterSet


class TicketsViewSet(viewsets.ModelViewSet):
    queryset = Tickets.objects.all()
    serializer_class = TicketsSerializer
