import streamlit as st
import pydeck as pdk
import json
from shapely.geometry import shape
import os
from gpt_engine.langchain_interface import GPTResponder

st.set_page_config(layout="wide")

# 사이드바 - API 키는 secrets.toml에 저장하므로 입력받지 않고 바로 사용
# 만약 시연용으로 직접 입력 받고 싶으면 아래 코드 참고
# api_key = st.sidebar.text_input("🔑 OpenAI API Key", type="password")
# if api_key:
#     os.environ["OPENAI_API_KEY"] = api_key

# secrets.toml에서 API 키 읽어서 환경변수 세팅
os.environ["OPENAI_API_KEY"] = st.secrets["openai"]["api_key"]

# 사이드바
st.sidebar.title("임시 메뉴바")
st.sidebar.write("여기에 메뉴나 필터, 설명 등 넣으세요.")

# 페이지 타이틀
st.title("전국 읍면동 위치 시각화")

# GeoJSON 파일 로딩
geojson_path = r"skorea-submunicipalities-2018-geo.json"
with open(geojson_path, 'r', encoding='utf-8') as f:
    geojson = json.load(f)

# 읍면동 중심 좌표 계산
locations = []
for feature in geojson['features']:
    geom = shape(feature['geometry'])
    centroid = geom.centroid
    locations.append({
        "name": feature['properties']['name_eng'],
        "lon": centroid.x,
        "lat": centroid.y,
    })

# 경계 레이어
boundary_layer = pdk.Layer(
    "GeoJsonLayer",
    {
        "type": "FeatureCollection",
        "features": geojson['features'],
    },
    stroked=True,
    filled=True,
    get_fill_color=[180, 220, 255, 80],
    get_line_color=[0, 0, 100],
    line_width_min_pixels=1,
    pickable=True,
    auto_highlight=True,
)

# 점 레이어
point_layer = pdk.Layer(
    "ScatterplotLayer",
    data=locations,
    get_position='[lon, lat]',
    get_radius=1000,
    get_fill_color=[255, 140, 0],
    pickable=True,
)

# 초기 뷰 상태
view_state = pdk.ViewState(
    latitude=34.8,
    longitude=127.3,
    zoom=8,
    pitch=30,
)

# 툴팁 설정
tooltip = {
    "html": "<b>{name}</b>",
    "style": {
        "backgroundColor": "white",
        "color": "black",
        "fontSize": "12px",
    },
}

# 지도 생성
deck = pdk.Deck(
    layers=[boundary_layer, point_layer],
    initial_view_state=view_state,
    map_style="mapbox://styles/mapbox/light-v9",
    tooltip=tooltip,
)

# 지도 렌더링
html = deck.to_html(as_string=True, notebook_display=False)
st.components.v1.html(html, height=900, scrolling=False)

# GPT 프롬프트 입력란
st.markdown("---")
prompt = st.text_input("💬 GPT 프롬프트를 입력하세요", placeholder="예: 전남에서 데이터 기반 프로젝트 아이디어는?")

if prompt:
    gpt = GPTResponder()  # api_key 전달 없음, 환경변수로 자동 인증
    with st.spinner("⏳ GPT 응답 생성 중..."):
        response = gpt.ask(prompt)
    st.subheader("🧠 GPT 응답")
    st.write(response)
