from django.apps import AppConfig


class EchoClientConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'echo_client'

    def ready(self):
        # Import signals or other startup code here if needed
        pass