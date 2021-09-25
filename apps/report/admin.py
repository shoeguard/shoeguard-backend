from django.contrib import admin
from django_restful_admin import admin as api_admin

from apps.report.models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'reporter',
        'address',
        'reported_device',
        'is_done',
    )


api_admin.site.register(Report)
