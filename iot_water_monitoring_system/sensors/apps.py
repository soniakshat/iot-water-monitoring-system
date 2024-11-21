from django.apps import AppConfig
import threading

class SensorsConfig(AppConfig):
    name = 'sensors'

    def ready(self):
        from .mqtt_client import start_mqtt_client
        threading.Thread(target=start_mqtt_client, daemon=True).start()
