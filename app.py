import streamlit as st
from logic import get_weather_forecast
from utils import get_coordinates

st.title("🌤️ Weather Insight")
city = st.text_input("都市名を入力してください")

if city:
    lat, lon = get_coordinates(city)
    if lat and lon:
        forecast_df = get_weather_forecast(lat, lon)
        st.subheader(f"{city} の天気予報")
        st.dataframe(forecast_df)
        st.line_chart(forecast_df[['temperature_2m', 'precipitation']])
    else:
        st.error("都市名が見つかりませんでした。")