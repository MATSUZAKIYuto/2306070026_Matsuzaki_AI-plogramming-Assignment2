import requests
import pandas as pd

def get_weather_forecast(lat, lon):
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&hourly=temperature_2m,weathercode"
        f"&daily=temperature_2m_max,temperature_2m_min"
        f"&timezone=Asia/Tokyo"
    )
    response = requests.get(url)
    data = response.json()

    # 時間別データ
    hourly = pd.DataFrame({
        "time": data["hourly"]["time"],
        "temperature_2m": data["hourly"]["temperature_2m"],
        "weathercode": data["hourly"]["weathercode"]
    })
    hourly["time"] = pd.to_datetime(hourly["time"])
    hourly["hour"] = hourly["time"].dt.hour
    hourly["date"] = hourly["time"].dt.date

    # 特定時間抽出
    selected_hours = hourly[hourly["hour"].isin([9, 12, 20])]
    selected_pivot = selected_hours.pivot_table(
        index="date", columns="hour", values=["temperature_2m", "weathercode"]
    )
    selected_pivot.columns = [f"{col[0]}_{col[1]}時" for col in selected_pivot.columns]
    selected_pivot.reset_index(inplace=True)

    # 日別データ
    daily = pd.DataFrame({
        "date": pd.to_datetime(data["daily"]["time"]).date,
        "最高気温": data["daily"]["temperature_2m_max"],
        "最低気温": data["daily"]["temperature_2m_min"]
    })

    # 結合
    summary = pd.merge(daily, selected_pivot, on="date", how="left")
    return summary