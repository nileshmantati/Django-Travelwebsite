from django.apps import AppConfig

class TravelConfig(AppConfig):
    name = 'travel'

    def ready(self):
        from .scheduler import start
        start()