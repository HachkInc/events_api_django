from django.db.models import Q
from requests import Response
from rest_framework import viewsets, status, permissions
from django_filters import rest_framework as filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView

from .serializers import EventsSerializer, TicketsSerializer, QrSerializer
from .models import Events, Tickets, User
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer, RegisterSerializer
from rest_framework import generics


class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class EventFilterSet(filters.FilterSet):

    word = filters.CharFilter(method='my_first_custom_filter', label="Search")
    class Meta:
        model1 = Events
        fields = ['word']

    def my_first_custom_filter(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) | Q(address__icontains=value) | Q(description__icontains=value)
        )

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