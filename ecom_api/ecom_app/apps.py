from django.apps import AppConfig


class EcomAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ecom_api.ecom_app"

    def ready(self):
        from . import signals