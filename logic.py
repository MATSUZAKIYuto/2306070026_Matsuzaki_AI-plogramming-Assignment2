import requests
import pandas as pd

def weathercode_to_description(code):
    mapping = {
        0: "快晴", 1: "晴れ", 2: "薄曇り", 3: "曇り",
        45: "霧", 48: "濃霧",
        51: "弱い霧雨", 53: "霧雨", 55: "強い霧雨",
        61: "弱い雨", 63: "雨", 65: "強い雨",
        71: "弱い雪", 73: "雪", 75: "強い雪",
        80: "にわか雨", 81: "にわか強雨", 82: "にわか豪雨",
        95: "雷雨", 96: "雷雨（弱い雹）", 99: "雷雨（強い雹）"
    }
    return mapping.get(code, "不明")

def weathercode_to_icon(code):
    icon_map = {
        0: "☀️", 1: "🌤️", 2: "⛅", 3: "☁️",
        45: "🌫️", 48: "🌫️",
        51: "🌦️", 53: "🌦️", 55: "🌧️",
        61: "🌧️", 63: "🌧️", 65: "🌧️",
        71: "🌨️", 73: "🌨️", 75: "❄️",
        80: "🌦️", 81: "🌧️", 82: "🌧️",
        95: "⛈️", 96: "⛈️", 99: "⛈️"
    }
    return icon_map.get(code, "❓")

def get_weather_forecast(lat, lon):
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&hourly=weathercode"
        f"&daily=temperature_2m_max,temperature_2m_min"
        f"&timezone=Asia/Tokyo"
    )
    response = requests.get(url)
    data = response.json()

    # 時間別データ（天気コードのみ）
    hourly = pd.DataFrame({
        "time": data["hourly"]["time"],
        "weathercode": data["hourly"]["weathercode"]
    })
    hourly["time"] = pd.to_datetime(hourly["time"])
    hourly["hour"] = hourly["time"].dt.hour
    hourly["date"] = hourly["time"].dt.date

    # 特定時間抽出（9時, 12時, 20時）
    selected_hours = hourly[hourly["hour"].isin([9, 12, 20])]
    selected_pivot = selected_hours.pivot_table(
        index="date", columns="hour", values="weathercode"
    )
    selected_pivot.columns = [f"{hour}時の天気" for hour in selected_pivot.columns]
    selected_pivot.reset_index(inplace=True)

    # 天気コード → 説明＋アイコン（同じ欄に統合）
    for col in selected_pivot.columns:
        if "時の天気" in col:
            selected_pivot[col] = selected_pivot[col].apply(
                lambda code: f"{weathercode_to_description(code)} {weathercode_to_icon(code)}"
            )

    # 日別データ（最高・最低気温）
    daily = pd.DataFrame({
        "date": pd.to_datetime(data["daily"]["time"]).date,
        "最高気温": data["daily"]["temperature_2m_max"],
        "最低気温": data["daily"]["temperature_2m_min"]
    })

    # 結合して最終データフレームに
    summary = pd.merge(daily, selected_pivot, on="date", how="left")
    return summary