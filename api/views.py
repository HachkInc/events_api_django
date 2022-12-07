from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from django_filters import rest_framework as filters
# from .serializers import UserSerializer
from .serializers import EventsSerializer, TicketsSerializer
from .models import Events, Tickets
# import QuerySet


# class UserViewSet(viewsets.ModelViewSet):
    # queryset = User.objects.all().order_by('name')
    # serializer_class = UserSerializer


class EventFilterSet(filters.FilterSet):
    class Meta:
        model = Events
        fields = {
            'title': ['exact'],    #Только точные совпадения
        }


class EventsViewSet(viewsets.ModelViewSet):
    queryset = Events.objects.all()
    serializer_class = EventsSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EventFilterSet
    # .filter(title__startswith='')   на всякий чтобы искать по началу


class TicketsViewSet(viewsets.ModelViewSet):
    queryset = Tickets.objects.all()
    serializer_class = TicketsSerializer
