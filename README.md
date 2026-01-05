# Smart Room Project - Smart Room Automation

This project is a comprehensive IoT application that simulates a smart room. It collects sensor data, communicates via MQTT protocol, stores this data in an InfluxDB time-series database, and visualizes it using a Streamlit dashboard.

## Features

- **Sensor Simulation:** Temperature, CO2, Humidity, and Smoke sensors.
- **Actuator Control:** Fan, Window, and Fire Alarm control.
- **MQTT Communication:** Real-time data flow between devices and the controller.
- **Data Logging:** Storage of time-series data using InfluxDB.
- **Smart Dashboard:** Real-time monitoring with Streamlit and AI-powered temperature forecasting using Prophet.
- **Unity Digital Twin:** A 3D environment that visualizes sensor data and allows for "Auto" or "Manual" control logic via a UI panel.

---

## 🛠️ Installation and Requirements

Before running the project, ensure the following components are installed.

### 1. Python Libraries
To install the necessary libraries, run the following command in the terminal from the project root directory:

```bash
pip install streamlit prophet plotly pandas paho-mqtt influxdb-client python-dotenv
```

### 2. InfluxDB Setup (for Mac OS)

This project uses InfluxDB v2 as its database. The easiest method for installation on macOS is using Homebrew.

1.  **Install via Homebrew:**
    ```bash
    brew update
    brew install influxdb
    ```

2.  **Start the Service:**
    To start InfluxDB in the background:
    ```bash
    brew services start influxdb
    ```
    *Alternatively, you can run `influxd` to start it temporarily.*

3.  **Initial Setup:**
    - Go to `http://localhost:8086` in your browser.
    - Click on the **"Get Started"** button.
    - Set a username and password.
    - **Organization Name:** `iot_project`
    - **Bucket Name:** `sensor_data`
    - Once setup is complete, copy the **API Token** provided. Do not lose this!

> **Note:** If you are using Windows, you can download the Windows binaries from the official InfluxDB website and run `influxd.exe`.

### 3. Unity 3D Digital Twin Setup
The project includes a Unity project folder representing the Digital Twin of the room.

1.  **Prerequisites:** Ensure you have Unity Hub and a recent version of the Unity Editor installed.
   
2.  **Open Project:**
   - Launch Unity Hub.
   - Click "Open" and select the Unity-Simulation (or your specific folder name) folder inside the repository.

3.  **Dependencies:**
   -The project uses the M2MqttUnity library (a wrapper for Paho MQTT). This is included in the Assets/ folder, so no external package installation is usually required.

4.  **Configuration:**

    - Open the main scene (Assets/Scenes/Home).
    - Select the SmartRoomController object in the Hierarchy.
    - In the Inspector panel, ensure the Broker Address matches the one used in Python (default: test.mosquitto.org).
    - You can toggle "Auto Mode" on/off from the Inspector or the in-game UI to switch between automated logic and manual control.
---

## ⚙️ Configuration (.env File)

Create a file named `.env` in the project's root directory (directly inside `SmartRoomProject`) if it doesn't already exist. Enter the credentials you defined during the InfluxDB setup:

```ini
INFLUX_URL=http://localhost:8086
INFLUX_TOKEN=Your_Copied_Long_Token_Here
INFLUX_ORG=iot_project
INFLUX_BUCKET=sensor_data
```

*Note: The project code uses `test.mosquitto.org` as the MQTT Broker. If you wish to use a local broker, you can update the `BROKER` variable in `main.py` and the `Broker Address` in the Unity Inspector.*

---

## ▶️ Running the Project

Step 1: Open your terminal and navigate to the project directory. To start the application, run the main file `main.py`:

```bash
cd Python-Files
python main.py
```

This command will:
1.  Start the sensor and environment simulation.
2.  Begin publishing data via MQTT.
3.  Automatically launch the **Streamlit Dashboard** in the background (a new tab will open in your browser).

If the Dashboard does not open automatically, you can run the following command in a separate terminal:
```bash
streamlit run Python-Files/dashboard.py
```

Step 2: Go back to the Unity Editor. Press the Play (▶) button at the top of the window.

The room will connect to the MQTT broker. You should see the sensor values update on the virtual UI panel, and the fan/windows react to the Python simulation's data.
---

## 📂 Project Structure

```
SmartRoomProject/
├── Unity-Files/
│   ├── Assets/
│   │   ├── Scripts/               # C# Scripts
│   │   │   ├── RoomController.cs
│   │   │   ├── AutomationToggle.cs
│   │   │   ├── UIManager.cs
│   │   │   └── ...                # Other helper scripts  
│   │   ├── Scenes/                # Unity Scenes
│   │   │   └── Home.unity
│   │   ├── M2MqttUnity/           # MQTT Wrapper Library
│   │   └── ...                    # Other Unity related files
│   ├── Packages/                  # Unity Package Manifests
│   └── ProjectSettings/           # Unity Project Settings
├── .env                    # Secrets and configuration
├── README.md               # Project documentation
└── Python-Files/           # Source code
    ├── main.py             # Main application (Starts simulation)
    ├── dashboard.py        # Streamlit interface
    ├── data_layer.py       # Database operations (InfluxDB)
    ├── comm_layer.py       # Communication layer (MQTT)
    ├── device_layer.py     # Sensor and actuator classes
    ├── control_layer.py    # Room control logic
    ├── unity.py            # Unity test/simulation client
    └── config.py           # Configuration file

```
