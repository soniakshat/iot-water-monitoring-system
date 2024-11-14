from django.apps import AppConfig

class SensorsConfig(AppConfig):
    name = 'sensors'

    def ready(self):
        pass  # No additional code needed here
