# import paho.mqtt.client as mqtt
# import json
# from .models import WaterQualityData
# import threading

# # MQTT broker details
# MQTT_BROKER = 'broker.emqx.io'
# MQTT_PORT = 1883
# MQTT_TOPIC = 'test/demo'

# # Define the callback for received messages
# def on_message(client, userdata, message):
#     print(f"Received message: {message.payload.decode()} on topic: {message.topic}")
    
#     # Import WaterQualityData inside the function to avoid AppRegistryNotReady error
#     from .models import WaterQualityData
    
#     try:
#         # Load JSON data and save it to the database
#         data = json.loads(message.payload.decode())
        
#         # Insert the parsed data into the WaterQualityData model
#         WaterQualityData.objects.create(
#             pH=data["pH"],
#             turbidity=data["Turbidity (NTU)"],
#             dissolved_oxygen=data["Dissolved Oxygen (mg/L)"],
#             conductivity=data["Conductivity (µS/cm)"],
#             temperature=data["Temperature (°C)"],
#             nitrate=data["Nitrate (mg/L)"],
#             phosphate=data["Phosphate (mg/L)"],
#             total_organic_carbon=data["Total Organic Carbon (mg/L)"],
#             chlorine=data["Chlorine (mg/L)"],
#             ammonium=data["Ammonium (mg/L)"],
#             heavy_metals=data["Heavy Metals (µg/L)"],
#             fluoride=data["Fluoride (mg/L)"],
#             oxidation_reduction_potential=data["Oxidation-Reduction Potential (mV)"],
#             biological_oxygen_demand=data["Biological Oxygen Demand (mg/L)"]
#         )
#         print("Water Quality Data saved to the database")
#     except json.JSONDecodeError as e:
#         print(f"Error decoding JSON: {e}")
#     except KeyError as e:
#         print(f"Missing data field in received message: {e}")

# # Set up the MQTT client instance and define the callback
# client = mqtt.Client("Django_Subscriber")  # No need for callback_api_version with version 1.6.1
# client.on_message = on_message

# # Function to connect and start the MQTT client
# def start_mqtt():
#     client.connect(MQTT_BROKER, MQTT_PORT)
#     client.subscribe(MQTT_TOPIC)
#     client.loop_forever()  # Loop forever to continuously listen for messages

# # Run MQTT client in a background thread with Django
# def run_mqtt_client():
#     mqtt_thread = threading.Thread(target=start_mqtt)
#     mqtt_thread.daemon = True  # Ensure thread terminates with the main program
#     mqtt_thread.start()
