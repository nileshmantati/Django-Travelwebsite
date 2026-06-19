import os
from django.apps import AppConfig

class BusAppConfig(AppConfig):
    name = 'bus_app'

    def ready(self):
        from .scheduler import start
        start()