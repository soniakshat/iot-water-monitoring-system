from django.db import models

class WaterQualityData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    pH = models.FloatField()
    turbidity = models.FloatField()  # NTU
    dissolved_oxygen = models.FloatField()  # mg/L
    conductivity = models.FloatField()  # µS/cm
    temperature = models.FloatField()  # °C
    nitrate = models.FloatField()  # mg/L
    phosphate = models.FloatField()  # mg/L
    total_organic_carbon = models.FloatField()  # mg/L
    chlorine = models.FloatField()  # mg/L
    ammonium = models.FloatField()  # mg/L
    heavy_metals = models.FloatField()  # µg/L
    fluoride = models.FloatField()  # mg/L
    oxidation_reduction_potential = models.FloatField()  # mV
    biological_oxygen_demand = models.FloatField()  # mg/L

    def __str__(self):
        return f"Water Quality at {self.timestamp}"
