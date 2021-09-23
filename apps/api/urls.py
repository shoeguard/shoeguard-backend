from apps.location_history.views import LocationHistoryViewSet
from apps.report.views import ReportViewSet
from apps.user.views import PhoneVerificationViewSet, UserViewSet
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

router = DefaultRouter(trailing_slash=False)
router.register(r'users', UserViewSet, basename='users')
router.register(
    r'phone-verification',
    PhoneVerificationViewSet,
    basename='phone_verification',
)
router.register(r'reports', ReportViewSet, basename='reports')
router.register(
    r'location-history',
    LocationHistoryViewSet,
    basename='location_histories',
)

urlpatterns = [
    path('token', TokenObtainPairView.as_view()),
    path('token/refresh', TokenRefreshView.as_view()),
    path('token/verify', TokenVerifyView.as_view())
]

urlpatterns += router.urls
