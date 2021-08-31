from django.contrib import admin
from django_restful_admin import admin as api_admin

from apps.location_history.models import LocationHistory

admin.site.register(LocationHistory)
api_admin.site.register(LocationHistory)
