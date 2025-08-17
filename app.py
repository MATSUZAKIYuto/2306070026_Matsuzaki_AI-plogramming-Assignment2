import streamlit as st
from logic import get_weather_forecast
from utils import get_coordinates

st.title("🌤️ 天気予報")
city = st.text_input("都市名をローマ字入力してください")

if city:
    lat, lon = get_coordinates(city)
    if lat and lon:
        forecast_df = get_weather_forecast(lat, lon)
        st.subheader(f"{city} の天気予報（日別）")
        st.dataframe(forecast_df)

        st.line_chart(forecast_df.set_index("date")[["最高気温", "最低気温"]])

        st.subheader(f"{city} の位置")
        st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}))
    else:
        st.error("都市名が見つかりませんでした。")

