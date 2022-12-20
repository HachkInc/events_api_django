from django.http import Http404, JsonResponse
from rest_framework import viewsets, status
from django_filters import rest_framework as filters
from .serializers import EventsSerializer, TicketsSerializer
from .models import Events, Tickets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import UserSerializer, RegisterSerializer
from rest_framework import generics
from django.contrib.auth.models import User
# from snippets.serializers import UserSerializer


# class UserDetail(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#     def get_object(self, pk):
#         try:
#             user = User.objects.get(pk=pk)
#             print(user)
#             return user
#         except User.DoesNotExist:
#             raise Http404
#
#     def list(self):
#         return self.queryset
#
#     def get(self, pk, format=None):
#         user = self.get_object(pk)
#         serializer = UserSerializer(user)
#         return Response(serializer.data)
#
#     def delete(self, request, pk, format=None):
#         user = self.get_object(pk)
#         user.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#     def patch(self, request, pk):
#         user = self.get_object(pk)
#
#         serializer = UserSerializer(user, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(201, data=serializer.data)
#         return JsonResponse(404, data="Wrong parameters. Not found")


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
