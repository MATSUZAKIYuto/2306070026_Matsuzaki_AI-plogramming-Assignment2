import requests
import pandas as pd

def get_weather_forecast(lat, lon):
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&hourly=temperature_2m,precipitation"
    )
    response = requests.get(url)
    data = response.json()

    hourly = data["hourly"]
    df = pd.DataFrame({
        "time": hourly["time"],
        "temperature_2m": hourly["temperature_2m"],
        "precipitation": hourly["precipitation"]
    })
    df["time"] = pd.to_datetime(df["time"])
    return df