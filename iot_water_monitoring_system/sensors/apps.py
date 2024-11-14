from django.apps import AppConfig

class SensorsConfig(AppConfig):
    name = 'sensors'

    def ready(self):
        from .mqtt_client import start_mqtt_client
        start_mqtt_client()  # Start the MQTT client when the app is ready
