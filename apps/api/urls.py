from apps.report.views import ReportViewSet
from apps.user.views import UserViewSet
from django.urls import path
from rest_framework import serializers
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

router = DefaultRouter(trailing_slash=False)
router.register(r'users', UserViewSet, basename='users')
router.register(r'reports', ReportViewSet, basename='reports')


class DocumentedTokenObtainPairView(TokenObtainPairView):
    class DocumentedTokenObtainPairSerializer(TokenObtainPairSerializer):
        refresh = serializers.CharField(read_only=True)
        access = serializers.CharField(read_only=True)

    serializer_class = DocumentedTokenObtainPairSerializer


urlpatterns = [
    path('token', DocumentedTokenObtainPairView.as_view()),
    path('token/refresh', TokenRefreshView.as_view()),
    path('token/verify', TokenVerifyView.as_view())
]

urlpatterns += router.urls
