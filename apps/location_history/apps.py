from django.apps import AppConfig
from django.db.models.signals import pre_save


class LocationHistoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.location_history'

    def ready(self):
        from apps.common.signals import geocode_pre_save_handler
        from apps.location_history.models import LocationHistory
        pre_save.connect(geocode_pre_save_handler, LocationHistory)
