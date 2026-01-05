from config import INFLUX_URL, INFLUX_TOKEN, INFLUX_ORG, INFLUX_BUCKET
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import pandas as pd

class InfluxService:
    def __init__(self, url, token, org, bucket):
        self.url = url
        self.token = token
        self.org = org
        self.bucket = bucket

        self.client = InfluxDBClient(url=url, token=token, org=org)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.query_api = self.client.query_api()

    def write_data(self, temperature, co2, smoke, humidity, fan_on, window_on, alarm_on):
        point = Point("sensor_readings") \
            .tag("oda", "salon") \
            .field("temperature", float(temperature)) \
            .field("co2", float(co2)) \
            .field("humidity", float(humidity)) \
            .field("smoke", int(smoke)) \
            .field("fan_on", bool(fan_on)) \
            .field("window_on", bool(window_on)) \
            .field("alarm_on", bool(alarm_on))

        self.write_api.write(bucket=self.bucket, org=self.org, record=point)

    def read_data(self, time_range="-30m"):
        query = f'''
        from(bucket: "{self.bucket}")
        |> range(start: {time_range})
        |> filter(fn: (r) => r._measurement == "sensor_readings")
        |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
        '''

        try:
            result = self.query_api.query_data_frame(query)

            if isinstance(result, list):
                df = pd.concat(result, ignore_index=True)
            else:
                df = result

            if not df.empty:
                df['_time'] = pd.to_datetime(df['_time'])
                df['_time'] = df['_time'].dt.tz_localize(None)
                return df

        except Exception as e:
            print("READ ERROR:", e)
        return pd.DataFrame()

    def close(self):
        self.client.close()

influx = InfluxService(INFLUX_URL, INFLUX_TOKEN, INFLUX_ORG, INFLUX_BUCKET)

def store_data(msg):
    try:
        influx.write_data(
            temperature=msg["temperature"], co2=msg["co2"], smoke=msg["smoke"], humidity=msg.get("humidity", 0),
            fan_on=msg.get("fan_on"), window_on=msg.get("window_on"), alarm_on=msg.get("alarm_on"))
        print("Recorded.")
    except Exception as e:
        print(f"Error: {e}")