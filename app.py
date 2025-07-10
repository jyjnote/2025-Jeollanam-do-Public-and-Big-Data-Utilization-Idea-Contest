import streamlit as st
import pydeck as pdk
import json
from shapely.geometry import shape
import os
from streamlit_option_menu import option_menu
from views import (
    index_view,
    recommendation_view,
    city_detail_view,
    report_view,
    simulation_view
)

# 페이지 설정
st.set_page_config(layout="wide")

# 🔒 API 키 환경 변수 설정
os.environ["MAPBOX_API_KEY"] = st.secrets["mapbox"]["token"]

# 📂 사이드 메뉴 (아이콘 포함)
with st.sidebar:
    st.markdown("## 📊 메뉴")
    menu = option_menu(
        menu_title=None,
        options=["정주지수", "정주지 추천", "도시별 상세보기", "정책 리포트", "정책 시뮬레이션"],
        icons=["bar-chart-line", "geo-alt", "building", "file-earmark-text", "cpu"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"background-color": "#1e1e1e"},
            "icon": {"color": "orange", "font-size": "18px"},
            "nav-link": {"color": "#ddd", "font-size": "16px", "text-align": "left"},
            "nav-link-selected": {"background-color": "#ffa500", "color": "black"},
        }
    )

# 메뉴 라우팅
if menu == "정주지수":
    index_view.render()
elif menu == "정주지 추천":
    recommendation_view.render()
elif menu == "도시별 상세보기":
    city_detail_view.render()
elif menu == "정책 리포트":
    report_view.render()
elif menu == "정책 시뮬레이션":
    simulation_view.render()

# 🗺️ 타이틀
st.title("전국 읍면동 위치 시각화")

# GeoJSON 불러오기
base_dir = os.path.dirname(__file__)
geojson_path = os.path.join(base_dir, "geo_jsons", "skorea-submunicipalities-2018-geo.json")

with open(geojson_path, 'r', encoding='utf-8') as f:
    geojson = json.load(f)

# 지역명 리스트
region_names = [f['properties']['name_eng'] for f in geojson['features']]
selected_region = st.sidebar.selectbox("🧭 읍면동 선택 (클릭 강조)", ["선택 안 함"] + region_names)

# 선택된 구역 필터링 및 중심 좌표 설정
highlight_layer = None
if selected_region == "선택 안 함":
    center_lat, center_lon, zoom = 34.8, 127.3, 8
else:
    filtered_features = [f for f in geojson['features'] if f['properties']['name_eng'] == selected_region]
    geom = shape(filtered_features[0]['geometry'])
    center_lat = geom.centroid.y
    center_lon = geom.centroid.x
    zoom = 12
    highlight_layer = pdk.Layer(
        "GeoJsonLayer",
        data={"type": "FeatureCollection", "features": filtered_features},
        stroked=True,
        filled=True,
        get_fill_color=[255, 140, 0, 160],   # 클릭 강조 색상
        get_line_color=[255, 255, 0],
        line_width_min_pixels=2,
        pickable=True,
    )

# 배경 전체 읍면동 경계 (hover 강조 포함)
background_layer = pdk.Layer(
    "GeoJsonLayer",
    data={"type": "FeatureCollection", "features": geojson['features']},
    stroked=True,
    filled=True,
    get_fill_color=[50, 50, 50, 30],     # 흐릿한 회색, 투명도 높음
    get_line_color=[100, 100, 100],
    line_width_min_pixels=0.5,
    pickable=True,
    auto_highlight=True,
    highlight_color=[255, 255, 0, 180]
)

# 툴팁
tooltip = {
    "html": "<b>{name}</b>",
    "style": {
        "backgroundColor": "white",
        "color": "black",
        "fontSize": "12px",
    },
}

# 지도 레이어 설정
layers = [background_layer]
if highlight_layer:
    layers.insert(1, highlight_layer)

deck = pdk.Deck(
    layers=layers,
    initial_view_state=pdk.ViewState(
        latitude=center_lat,
        longitude=center_lon,
        zoom=zoom,
        pitch=30,
    ),
    map_style="mapbox://styles/mapbox/dark-v9",
    tooltip=tooltip,
)

# 지도 렌더링
html = deck.to_html(as_string=True, notebook_display=False)
st.components.v1.html(html, height=900, scrolling=False)
