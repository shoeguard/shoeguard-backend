from django.apps import AppConfig


class LocationHistoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.location_history'

    def ready(self):
        import apps.location_history.signals
