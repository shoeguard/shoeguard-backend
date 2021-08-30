from django.contrib import admin
from django_restful_admin import admin as api_admin

from apps.report.models import Report

admin.site.register(Report)
api_admin.site.register(Report)
