from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import Http404, HttpResponse
from drf_yasg import renderers, openapi
from drf_yasg.utils import swagger_auto_schema
from requests import Response
from rest_framework import viewsets, status, permissions, schemas
from django_filters import rest_framework as filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action, api_view, renderer_classes
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
    word = filters.CharFilter(method='filter_by_word', label="Search")

    class Meta:
        model1 = Events
        fields = ['word']

    def filter_by_word(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) | Q(address__icontains=value) | Q(description__icontains=value)
        )


#
# class TicketFilterSet(filters.FilterSet):
#     # ids = filters.CharFilter(method='filter_by_ids', label="Search")
#
#     # by_id = filters.CharFilter(method='filter_by_id', label="Search")
#
#     class Meta:
#         model = Tickets
#         # fields = ['event_id_id', 'user_id_id', 'id']
#         fields = ['event_id_id', 'user_id_id']
#
#     def filter_by_ids(self, queryset, name, value):
#         return queryset.filter(
#             Q(user_id=value) & Q(event_id=value)
#         )

# def filter_by_id(self, queryset, name, value):
#     return queryset.filter(
#         Q(user_id=value)
#     )


class EventsViewSet(viewsets.ModelViewSet):
    queryset = Events.objects.all()
    serializer_class = EventsSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EventFilterSet


class TicketsViewSet(viewsets.ModelViewSet):
    queryset = Tickets.objects.all()
    serializer_class = TicketsSerializer
    # filter_backends = (filters.DjangoFilterBackend,)
    # filterset_class = TicketFilterSet

    # def destroy(self, request, *args, **kwargs):
    #     ticket = Tickets.objects.get(event_id=request.data['event_id'], user_id=request.data['user_id'])
    #     self.perform_destroy(ticket)
    #     return Response(status=status.HTTP_204_NO_CONTENT)


class UserDetailAPIView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class QrDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = QrSerializer


@swagger_auto_schema(method='delete', operation_description="Delete ticket", request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'event_id': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        'user_id': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
    },
    responses={404: "Ticket not found", 204: "Ticket found and deleted"}
))
@api_view(['delete'])
@renderer_classes([renderers.OpenAPIRenderer, renderers.SwaggerUIRenderer])
def delete_by_ids(request, pk=None):
    generator = schemas.SchemaGenerator(title='Delete by ids')
    try:
        ticket = Tickets.objects.get(event_id=request.data['event_id'], user_id=request.data['user_id'])
        ticket.delete()
        return HttpResponse(status=204)
    except ObjectDoesNotExist:
        return HttpResponse(status=404)
