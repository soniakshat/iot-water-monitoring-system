# IoT Water Monitoring System

This project is an IoT-based water monitoring system that uses MQTT for communication. It collects data from sensors and publishes it to an MQTT broker.

## Prerequisites

- Python 3.12 or later
- Poetry for dependency management

## Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/soniakshat/iot-water-monitoring-system.git
   cd iot-water-monitoring-system
   ```

2. **Install Poetry**

   If you haven't installed Poetry yet, you can do so by running:

   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. **Install Dependencies**

   Use Poetry to install the project dependencies:

   ```bash
   poetry install
   ```

4. **Activate the Virtual Environment**

   Activate the virtual environment created by Poetry:

   ```bash
   poetry shell
   ```

5. **Run the MQTT Server**

   Execute the MQTT server script:

   ```bash
   python mqtt_server.py
   ```

## Configuration

- **MQTT Broker**: The default broker is set to `broker.emqx.io` on port `1883`. You can change these settings in `mqtt_server.py`.

- **Topic**: The default topic is `test/demo`. Modify it as needed in `mqtt_server.py`.

## Contributing

Feel free to submit issues or pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License.
