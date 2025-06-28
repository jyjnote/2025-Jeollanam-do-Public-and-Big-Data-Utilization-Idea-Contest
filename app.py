import streamlit as st
import pydeck as pdk
import json
from shapely.geometry import shape

st.set_page_config(layout="wide")

st.sidebar.title("임시 메뉴바")
st.sidebar.write("여기에 메뉴나 필터, 설명 등 넣으세요.")

st.title("전국 읍면동 위치 시각화")

geojson_path = r"skorea-submunicipalities-2018-geo.json"

with open(geojson_path, 'r', encoding='utf-8') as f:
    geojson = json.load(f)

locations = []
for feature in geojson['features']:
    geom = shape(feature['geometry'])
    centroid = geom.centroid
    locations.append({
        "name": feature['properties']['name_eng'],
        "lon": centroid.x,
        "lat": centroid.y,
    })

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

point_layer = pdk.Layer(
    "ScatterplotLayer",
    data=locations,
    get_position='[lon, lat]',
    get_radius=1000,
    get_fill_color=[255, 140, 0],
    pickable=True,
)

text_layer = pdk.Layer(
    "TextLayer",
    data=locations,
    get_position='[lon, lat]',
    get_text='name',
    get_size=12,
    get_color=[0, 0, 0],
    get_angle=0,
    get_text_anchor='"middle"',
    get_alignment_baseline='"center"',
)

view_state = pdk.ViewState(
    latitude=34.8,    # 전라남도 중심 위도
    longitude=127.3,  # 전라남도 중심 경도
    zoom=8,
    pitch=30,
)

deck = pdk.Deck(
    layers=[boundary_layer, point_layer, text_layer],
    initial_view_state=view_state,
    map_style="mapbox://styles/mapbox/light-v9",
)

html = deck.to_html(as_string=True, notebook_display=False)
st.components.v1.html(html, height=900, scrolling=False)
