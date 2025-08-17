import streamlit as st
from logic import get_weather_forecast
from utils import get_coordinates

st.set_page_config(page_title="天気予報", page_icon="🌤️", layout="wide")

st.title("🌤️ 天気予報")
st.caption("都市名を英語で入力してください（例：Tokyo, Osaka）")

# ユーザー入力
city = st.text_input("都市名を入力", placeholder="例：Tokyo")

if city:
    lat, lon = get_coordinates(city)
    if lat and lon:
        # 地図表示
        st.subheader(f"{city} の位置")
        st.map(data={"lat": [lat], "lon": [lon]})

        # 天気予報取得
        forecast_df = get_weather_forecast(lat, lon)

        # 表形式で表示
        st.subheader(f"{city} の天気予報（日別）")
        st.dataframe(forecast_df, use_container_width=True)

        """# グラフ表示（最高・最低気温）
        st.subheader("📈 気温の推移")
        st.line_chart(forecast_df.set_index("date")[["最高気温", "最低気温"]])"""

        """# 時間別天気（アイコン付き）を日別で表示
        st.subheader("🕒 時間別の天気（9時・12時・20時）")
        for _, row in forecast_df.iterrows():
            st.markdown(f"### {row['date']}")
            cols = st.columns(3)
            for i, hour in enumerate([9, 12, 20]):
                desc_with_icon = row.get(f"{hour}時の天気", "不明")
                cols[i].markdown(f"{hour}時：{desc_with_icon}")
        """
    else:
        st.error("都市名が見つかりませんでした。英語表記で入力してください。")