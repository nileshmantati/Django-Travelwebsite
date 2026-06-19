import os
from django.apps import AppConfig

class TrainAppConfig(AppConfig):
    name = 'train_app'

    def ready(self):
        from .scheduler import start
        start()