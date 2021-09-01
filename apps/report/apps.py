from django.apps import AppConfig
from django.db.models.signals import pre_save


class ReportConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.report'

    def ready(self):
        from apps.common.signals import geocode_pre_save_handler
        from apps.report.models import Report
        pre_save.connect(geocode_pre_save_handler, Report)
