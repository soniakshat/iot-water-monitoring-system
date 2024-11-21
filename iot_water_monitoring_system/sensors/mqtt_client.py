import paho.mqtt.client as mqtt
import json
from .models import WaterQualityData
from .analysis import perform_incremental_pca_and_cca
import threading

# MQTT broker details
MQTT_BROKER = 'broker.emqx.io'
MQTT_PORT = 1883
MQTT_TOPIC = 'test/demo'

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.subscribe(MQTT_TOPIC)
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    # print(f"Received message: {msg.payload.decode()} on topic: {msg.topic}")
    try:
        # Parse JSON data
        data = json.loads(msg.payload.decode())
        
        # Save data to WaterQualityData model
        WaterQualityData.objects.create(
            pH=data["pH"],
            turbidity=data["Turbidity (NTU)"],
            dissolved_oxygen=data["Dissolved Oxygen (mg/L)"],
            conductivity=data["Conductivity (µS/cm)"],
            temperature=data["Temperature (°C)"],
            nitrate=data["Nitrate (mg/L)"],
            phosphate=data["Phosphate (mg/L)"],
            total_organic_carbon=data["Total Organic Carbon (mg/L)"],
            chlorine=data["Chlorine (mg/L)"],
            ammonium=data["Ammonium (mg/L)"],
            heavy_metals=data["Heavy Metals (µg/L)"],
            fluoride=data["Fluoride (mg/L)"],
            oxidation_reduction_potential=data["Oxidation-Reduction Potential (mV)"],
            biological_oxygen_demand=data["Biological Oxygen Demand (mg/L)"]
        )

        # Perform Incremental PCA and CCA
        perform_incremental_pca_and_cca()
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except KeyError as e:
        print(f"Missing data field in received message: {e}")

# Set up the MQTT client instance and define the callback
client = mqtt.Client("Django_Subscriber")
client.on_connect = on_connect
client.on_message = on_message

def start_mqtt_client():
    client.connect(MQTT_BROKER, MQTT_PORT)
    client.loop_start()
