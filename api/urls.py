# myapi/urls.py
from django.urls import include, path
from rest_framework import routers
from . import views
from rest_framework_simplejwt import views as jwt_views



router = routers.DefaultRouter()
router.register(r'events', views.EventsViewSet)
router.register(r'tickets', views.TicketsViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('auth/register', views.RegisterUserAPIView.as_view()),
    path('auth/login', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
]
