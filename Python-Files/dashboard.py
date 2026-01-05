import streamlit as st
from prophet import Prophet
import plotly.graph_objs as go
import time
import pandas as pd
from datetime import datetime, timedelta
from config import *
from data_layer import InfluxService

st.set_page_config(page_title="Smart System Panel", layout="wide")
st.title("Smart Room Automation and Security Monitoring System")
st.markdown("---")
DASHBOARD_REFRESH = 2
FORECAST_PERIODS = 5
DATA_RANGE = "-30m"

try:
    influx = InfluxService(INFLUX_URL, INFLUX_TOKEN, INFLUX_ORG, INFLUX_BUCKET)
except Exception as e:
    st.error(f"Database connection error: {e}")
    st.stop()


def get_ai_forecast(data):
    try:
        df_ai = data[['_time', 'temperature']].rename(columns={'_time': 'ds', 'temperature': 'y'})
        df_ai['ds'] = df_ai['ds'].dt.tz_localize(None)
        m = Prophet()
        m.fit(df_ai)
        future = m.make_future_dataframe(periods=FORECAST_PERIODS, freq='min')
        forecast = m.predict(future)
        return forecast
    except Exception as e:
        print(f"AI Forecast error: {e}")
        return None


if 'last_ai_run' not in st.session_state:
    st.session_state.last_ai_run = datetime.now() - timedelta(minutes=10)
if 'cached_forecast' not in st.session_state:
    st.session_state.cached_forecast = None

main_placeholder = st.empty()

while True:
    df = influx.read_data(DATA_RANGE)
    unique_id = time.time()

    with main_placeholder.container():

        if not df.empty and len(df) > 1:
            last_row = df.iloc[-1]

            cur_temp = last_row.get('temperature', 0)
            cur_co2 = last_row.get('co2', 0)
            hum_val = last_row.get('humidity', 0)
            is_fire = bool(last_row.get('smoke', 0))

            fan_is_on = bool(last_row.get('fan_on', False))
            window_is_open = bool(last_row.get('window_on', False))
            alarm_is_active = bool(last_row.get('alarm_on', False))

            fan_status_txt = "ON" if fan_is_on else "OFF"
            window_status_txt = "OPEN" if window_is_open else "CLOSED"
            alarm_status_txt = "ACTIVE" if alarm_is_active else "INACTIVE"

            time_since_last = (datetime.now() - st.session_state.last_ai_run).total_seconds()
            if len(df) > 20 and (st.session_state.cached_forecast is None or time_since_last > 300):
                st.session_state.cached_forecast = get_ai_forecast(df)
                st.session_state.last_ai_run = datetime.now()

            if is_fire or alarm_is_active:
                st.error("EMERGENCY: FIRE DETECTED! ")
            else:
                st.write("")

            c1, c2, c3, c4, c5 = st.columns(5)

            c1.metric("Temperature", f"{cur_temp:.1f} °C", delta_color="inverse")
            c2.metric("CO2", f"{cur_co2:.0f} ppm", delta_color="inverse")
            c3.metric("Humidity", f"{hum_val:.1f} %")

            c4.metric(
                label="Fan Status",
                value=fan_status_txt,
                delta="Cooling" if fan_is_on else "Idle",
                delta_color="normal" if fan_is_on else "off"
            )

            c5.metric(
                label="Window",
                value=window_status_txt,
                delta="Ventilating" if window_is_open else "Locked",
                delta_color="normal" if window_is_open else "off"
            )

            st.markdown("---")

            if alarm_is_active:
                st.warning(f"Fire Alarm: {alarm_status_txt}")

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Temperature & AI Forecast")
                fig = go.Figure()
                fig.add_trace(
                    go.Scatter(x=df['_time'], y=df['temperature'], name='Temperature', line=dict(color='blue', width=2)
                               ))

                if st.session_state.cached_forecast is not None:
                    ai_forecast = st.session_state.cached_forecast
                    fig.add_trace(go.Scatter(x=ai_forecast['ds'], y=ai_forecast['yhat'], name='AI Forecast',
                                             line=dict(color='red', dash='dot', width=2)
                                             ))

                fig.add_hline(y=25.0, line_dash="dot", line_color="orange",
                              annotation_text="Fan ON Limit (25°C)")
                fig.add_hline(y=22.0, line_dash="dot", line_color="green",
                              annotation_text="Fan OFF Limit (22°C)")

                fig.update_layout(yaxis_title="Temperature (°C)", xaxis_title="Time", hovermode='x unified')

                st.plotly_chart(fig, width="stretch", key=f"temp_{unique_id}")

            with col2:
                st.subheader("Air Quality & Humidity")
                fig2 = go.Figure()

                fig2.add_trace(go.Scatter(x=df['_time'], y=df['co2'], name='CO2', line=dict(color='grey', width=2),
                                          fill='tozeroy'))

                fig2.add_trace(go.Scatter(x=df['_time'], y=df['humidity'], name='Humidity', yaxis='y2',
                                          line=dict(color='cyan', width=2)))

                fig2.add_hline(y=550.0, line_dash="dot", line_color="orange",
                               annotation_text="Window OPEN Limit (550 ppm)")
                fig2.add_hline(y=500.0, line_dash="dot", line_color="green",
                               annotation_text="Window CLOSE Limit (500 ppm)")

                fig2.update_layout(
                    yaxis=dict(title='CO2 (ppm)'),
                    yaxis2=dict(title='Humidity (%)', overlaying='y', side='right'),
                    xaxis_title="Time",
                    hovermode='x unified'
                )

                st.plotly_chart(fig2, width="stretch", key=f"co2_{unique_id}")

            st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        else:
            st.info("Waiting for data from sensors...")

    time.sleep(DASHBOARD_REFRESH)