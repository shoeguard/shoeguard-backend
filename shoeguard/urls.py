"""shoeguard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from apps.api.urls import urlpatterns as api_urlpatterns
from django.contrib import admin
from django.urls import include, path
from django_restful_admin import admin as api_admin
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)

urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/',
         SpectacularSwaggerView.as_view(),
         name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(), name='redoc'),
    path('admin/', admin.site.urls),
    path('api/v1/admin/', api_admin.site.urls),
    path('api/v1/', include(api_urlpatterns)),
]
