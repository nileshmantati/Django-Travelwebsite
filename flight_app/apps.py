from django.apps import AppConfig


class FlightAppConfig(AppConfig):
    name = 'flight_app'

    def ready(self):
        from .scheduler import start
        start()