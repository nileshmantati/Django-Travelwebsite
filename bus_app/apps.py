import os
from django.apps import AppConfig

class BusAppConfig(AppConfig):
    name = 'bus_app'

    def ready(self):
        if os.environ.get('RUN_MAIN') == 'true':
            from .scheduler import start
            start()