# 2306070026_Matsuzaki_AI-plogramming-Assignment2

# 🌤️ 天気予報アプリ（Weather Insight）

## 📌 概要

このアプリは、ユーザーが都市名（英語）を入力すると、Open-Meteo API を利用してその地域の天気予報を表示する
1 日の最高・最低気温に加え、9 時・12 時・20 時の天気（絵文字付き）を表示します。都市の位置も地図上に表示される

## 🧪 使用 API

- [Open-Meteo Forecast API](https://open-meteo.com/en/features)（API キー不要）
- [Open-Meteo Geocoding API](https://open-meteo.com/en/docs/geocoding-api)

## 🖥️ 使用技術

- Python
- Streamlit
- Pandas
- Open-Meteo API

3. 📦 ファイル構成
   .
   ├── app.py # Streamlit UI と処理の起点
   ├── utils.py # 都市名 → 緯度経度変換（Geocoding）
   ├── logic.py # 天気 API 呼び出しと整形処理
   ├── assets/
   │ └── code_diagram.png # コード構成図
   └

ブロック図 1.png

コード図.png
