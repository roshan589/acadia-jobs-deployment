from django.apps import AppConfig


class JobportalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'jobportal'

    def ready(self):
        import jobportal.signals  # import signals so Django registers them
