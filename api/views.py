from requests import Response

from rest_framework import viewsets, status
from django_filters import rest_framework as filters
from .serializers import EventsSerializer, TicketsSerializer, QrSerializer
from .models import Events, Tickets, User
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer, RegisterSerializer
from rest_framework import generics
from django.contrib.auth import get_user_model


class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


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


class UserDetailAPIView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class QrDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = QrSerializer

