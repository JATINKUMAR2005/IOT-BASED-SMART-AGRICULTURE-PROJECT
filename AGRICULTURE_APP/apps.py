import sys
import threading

from django.apps import AppConfig


class AgricultureAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'AGRICULTURE_APP'

    def ready(self):
        if 'runserver' in sys.argv:
            from .sensor_reader import serial_to_db
            thread = threading.Thread(target=serial_to_db, daemon=True)
            thread.start()

