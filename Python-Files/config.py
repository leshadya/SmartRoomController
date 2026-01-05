import os
from dotenv import load_dotenv

load_dotenv()

INFLUX_URL = os.getenv("INFLUX_URL", "http://localhost:8086")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN")
INFLUX_ORG = os.getenv("INFLUX_ORG")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET")

DATA_RANGE = "-30m"
DASHBOARD_REFRESH = 2
FORECAST_PERIODS = 5