import paho.mqtt.client as mqtt
import time
import iot_server as iot

# MQTT broker details
broker = "broker.emqx.io"  # Use a public broker or your own local broker
port = 1883  # Default MQTT port
topic = "test/demo"  # Topic to publish to

# Create a client instance
client = mqtt.Client("Publisher")

# Connect to the broker
client.connect(broker, port)

# Publish messages to the topic
try:
    while True:
        message = iot.get_data()
        client.publish(topic, message)
        print(f"Published message: {message}")
        time.sleep(2)
except KeyboardInterrupt:
    print("Publisher stopped")
finally:
    client.disconnect()
