import os
import django
import random
from datetime import datetime, timedelta

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iot_water_monitoring_system.settings')
django.setup()

from sensors.models import WaterQualityData

# Generate dummy data
def create_dummy_data():
    for _ in range(10):  # Add 10 records
        WaterQualityData.objects.create(
            timestamp=datetime.now() - timedelta(days=random.randint(0, 30)),
            pH=round(random.uniform(3.0, 10.0), 2),
            turbidity=round(random.uniform(10.0, 150.0), 2),
            dissolved_oxygen=round(random.uniform(0.0, 12.0), 2),
            conductivity=round(random.uniform(500.0, 5000.0), 2),
            temperature=round(random.uniform(5.0, 35.0), 2),
            nitrate=round(random.uniform(1.0, 50.0), 2),
            phosphate=round(random.uniform(0.1, 5.0), 2),
            total_organic_carbon=round(random.uniform(0.0, 30.0), 2),
            chlorine=round(random.uniform(0.0, 5.0), 2),
            ammonium=round(random.uniform(0.0, 10.0), 2),
            heavy_metals=round(random.uniform(0.0, 200.0), 2),
            fluoride=round(random.uniform(0.0, 5.0), 2),
            oxidation_reduction_potential=round(random.uniform(-500.0, 500.0), 2),
            biological_oxygen_demand=round(random.uniform(0.0, 50.0), 2),
        )
    print("Dummy data added successfully!")

# Run the function
if __name__ == '__main__':
    create_dummy_data()
