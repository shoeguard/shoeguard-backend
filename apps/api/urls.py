from apps.user.views import UserViewSet
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

router = DefaultRouter(trailing_slash=False)
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('token', TokenObtainPairView.as_view()),
    path('token/refresh', TokenRefreshView.as_view()),
    path('token/verify', TokenVerifyView.as_view())
]

urlpatterns += router.urls
