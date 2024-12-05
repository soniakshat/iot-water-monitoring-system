import random
import time
import json


# Function to simulate data under normal water quality conditions
def generate_normal_conditions():
    temperature = round(random.uniform(15, 25), 2)
    dissolved_oxygen = round(10 - 0.25 * (temperature - 15), 2)

    return {
        "pH": round(random.uniform(6.5, 8.5), 2),
        "Turbidity (NTU)": round(random.uniform(0, 5), 2),
        "Dissolved Oxygen (mg/L)": dissolved_oxygen,
        "Conductivity (µS/cm)": round(random.uniform(100, 500), 2),
        "Temperature (°C)": temperature,
        "Nitrate (mg/L)": round(random.uniform(0, 2), 2),
        "Phosphate (mg/L)": round(random.uniform(0, 0.5), 2),
        "Total Organic Carbon (mg/L)": round(random.uniform(0, 5), 2),
        "Chlorine (mg/L)": round(random.uniform(0, 1), 2),
        "Ammonium (mg/L)": round(random.uniform(0, 1), 2),
        "Heavy Metals (µg/L)": round(random.uniform(0, 10), 2),
        "Fluoride (mg/L)": round(random.uniform(0.5, 1.5), 2),
        "Oxidation-Reduction Potential (mV)": round(random.uniform(200, 400), 2),
        "Biological Oxygen Demand (mg/L)": round(random.uniform(1, 5), 2),
    }



# Function to simulate data under abnormal water quality conditions
def generate_abnormal_conditions():
    return {
        "pH": round(random.uniform(3, 5), 2),  # Low pH indicating acidification
        "Turbidity (NTU)": round(random.uniform(50, 150), 2),  # High turbidity indicating pollution
        "Dissolved Oxygen (mg/L)": round(random.uniform(0, 3), 2),  # Low oxygen level
        "Conductivity (µS/cm)": round(random.uniform(2000, 5000), 2),  # High conductivity
        "Temperature (°C)": round(random.uniform(30, 40), 2),  # High temperature
        "Nitrate (mg/L)": round(random.uniform(10, 50), 2),  # High nitrate indicating contamination
        "Phosphate (mg/L)": round(random.uniform(1, 5), 2),  # High phosphate
        "Total Organic Carbon (mg/L)": round(random.uniform(10, 30), 2),  # High TOC
        "Chlorine (mg/L)": round(random.uniform(2, 5), 2),  # High chlorine
        "Ammonium (mg/L)": round(random.uniform(5, 10), 2),  # High ammonium
        "Heavy Metals (µg/L)": round(random.uniform(50, 200), 2),  # High levels of heavy metals
        "Fluoride (mg/L)": round(random.uniform(3, 5), 2),  # High fluoride
        "Oxidation-Reduction Potential (mV)": round(random.uniform(-200, 0), 2),  # Low ORP
        "Biological Oxygen Demand (mg/L)": round(random.uniform(20, 50), 2),
        # High BOD indicating high organic pollution
    }


# # Function to simulate mixed conditions, starting with normal and then switching to abnormal
# def generate_mixed_conditions(switch_time=10):
#     start_time = time.time()
#     while True:
#         current_time = time.time()
#         # Switch to abnormal after the specified switch time
#         if current_time - start_time < switch_time:
#             sensor_data = generate_normal_conditions()
#             print("Normal conditions:")
#         else:
#             sensor_data = generate_abnormal_conditions()
#             print("Abnormal conditions:")
#         sensor_data_json = json.dumps(sensor_data, indent=4)
#         print(sensor_data_json)
#         time.sleep(1)  # Generate data every second


def get_data():
    seed = random.random() * 10
    if seed // 2 != 0.0:
        return json.dumps(generate_normal_conditions(), indent=4)
    else:
        return json.dumps(generate_abnormal_conditions(), indent=4)


# # Function to simulate and print data under normal conditions indefinitely
# def simulate_normal():
#     while True:
#         sensor_data = generate_normal_conditions()
#         print("Normal conditions:")
#         print(json.dumps(sensor_data, indent=4))
#         time.sleep(1)  # Generate data every second


# # Function to simulate and print data under abnormal conditions indefinitely
# def simulate_abnormal():
#     while True:
#         sensor_data = generate_abnormal_conditions()
#         print("Abnormal conditions:")
#         print(json.dumps(sensor_data, indent=4))
#         time.sleep(1)  # Generate data every second


# Example usage
if __name__ == "__main__":
    # Uncomment one of the following lines to test each scenario
    # simulate_normal()  # Simulate normal conditions
    # simulate_abnormal()  # Simulate abnormal conditions
    generate_mixed_conditions(switch_time=10)
