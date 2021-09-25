from django.contrib import admin
from django_restful_admin import admin as api_admin

from apps.location_history.models import LocationHistory


@admin.register(LocationHistory)
class LocationHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'reporter',
        'address',
    )


api_admin.site.register(LocationHistory)
