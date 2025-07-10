import streamlit as st
import pandas as pd
import random
import plotly.graph_objects as go

# 이유 생성 함수
def get_reason(goal, value):
    if goal == "의료 접근성":
        return (
            f"이 지역은 의료 인프라가 잘 갖춰져 있습니다. "
            f"총 {value}개의 병의원 및 보건소가 운영 중이며, 이는 인구 대비 의료 접근성이 높은 편입니다. "
            f"따라서 응급상황 대응력과 일상적 건강관리 여건이 뛰어납니다. "
            f"**의료 사각지대 없는 정착을 원하는 고령자나 만성질환자에게 특히 적합한 지역입니다.**"
        )
    elif goal == "교육":
        return (
            f"이 지역은 교육 환경이 양호한 수준입니다. "
            f"학급당 평균 학생 수가 {value}명으로, 전국 평균보다 낮아 교사 1인당 학생 수 비율이 낮습니다. "
            f"이로 인해 집중도 높은 수업 환경이 조성됩니다. "
            f"**자녀 교육을 중시하는 가족 단위 정주자에게 유리한 선택지입니다.**"
        )
    elif goal == "생활비":
        return (
            f"이 지역은 비교적 저렴한 생활비 수준을 유지하고 있습니다. "
            f"평균 월세가 {value}만원으로 전라남도 평균보다 낮은 수준입니다. "
            f"이는 주거 안정성과 경제적 효율성을 동시에 제공합니다. "
            f"**정착 초기 비용을 절감하고 싶은 청년층이나 은퇴 세대에게 적합합니다.**"
        )
    elif goal == "기후":
        return (
            f"이 지역은 기후 조건이 안정적입니다. "
            f"연평균 기온이 {value}°C로, 사계절 중 극단적인 온도 변화가 적고 해양성 기후 영향으로 습도도 일정합니다. "
            f"쾌적한 날씨가 일상생활의 만족도를 높입니다. "
            f"**기후 민감도가 높은 고령자나 자연친화적 생활을 추구하는 이들에게 추천됩니다.**"
        )
    elif goal == "문화시설":
        return (
            f"이 지역은 다양한 문화 인프라가 구축돼 있습니다. "
            f"도서관, 문화센터, 체육시설 등 문화시설 수가 {value}개로, 주민들의 여가 및 문화 향유 기회를 제공합니다. "
            f"이는 정주지의 삶의 질에 긍정적으로 기여합니다. "
            f"**삶의 여유와 활동적 라이프스타일을 중시하는 정주자에게 적합합니다.**"
        )
    return ""

def get_value(goal):
    if goal == "의료 접근성":
        return random.randint(5, 15)
    elif goal == "교육":
        return random.randint(15, 30)
    elif goal == "생활비":
        return random.randint(20, 40)
    elif goal == "기후":
        return round(random.uniform(12.5, 14.5), 1)
    elif goal == "문화시설":
        return random.randint(2, 10)
    return 0

# Streamlit 앱
def render():
    st.subheader("🤝 전라남도 정주지 추천 (읍면동 단위)")

    goals = st.multiselect(
        "중요하게 생각하는 정주 조건을 모두 선택하세요:",
        ["의료 접근성", "교육", "생활비", "기후", "문화시설"],
        default=["의료 접근성"]
    )

    if not goals:
        st.warning("📌 하나 이상의 조건을 선택해주세요.")
        return

    eupmyeondong_data = pd.DataFrame({
        "지역": ["순천시 조례동", "여수시 소라면", "목포시 상동", "해남군 해남읍", "곡성군 옥과면"],
        "lat": [34.9506, 34.8284, 34.8122, 34.5742, 35.2483],
        "lon": [127.4871, 127.6427, 126.3937, 126.5988, 127.2423],
    })
    selected_row = eupmyeondong_data.sample(1).iloc[0]

    st.success(f"🏠 추천 지역: **{selected_row['지역']}**")
    st.map(pd.DataFrame({"lat": [selected_row["lat"]], "lon": [selected_row["lon"]]}))

    st.markdown("### 📋 조건별 분석 및 해설")
    records = []
    for goal in goals:
        value = get_value(goal)
        importance = random.randint(1, 5)
        reason = get_reason(goal, value)
        records.append({
            "조건": goal,
            "수치": value,
            "중요도": importance
        })
        with st.expander(f"🔍 {goal} 해설"):
            st.markdown(reason)

    df = pd.DataFrame(records)

    st.markdown("### 📌 조건별 주요 수치")
    card_cols = st.columns(len(df))
    for col, row in zip(card_cols, df.itertuples()):
        with col:
            st.metric(label=row.조건, value=row.수치)

    st.markdown("### 📊 시각적 비교 대시보드")
    col1, col2 = st.columns(2)

    # ▶️ Plotly 도넛 그래프 (조건 수치)
    with col1:
        st.markdown("#### 🍩 조건 수치 비율 (도넛형)")
        fig_donut = go.Figure(go.Pie(
            labels=df["조건"],
            values=df["수치"],
            hole=0.5,
            textinfo="label+percent"
        ))
        fig_donut.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=400)
        st.plotly_chart(fig_donut, use_container_width=True)

    # ▶️ Plotly Radar Chart (중요도 시각화)
    with col2:
        st.markdown("#### 🔷 중요도 레이더 (육각형 형태)")
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=df["중요도"],
            theta=df["조건"],
            fill='toself',
            name='중요도'
        ))
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 5])
            ),
            showlegend=False,
            height=400
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    st.caption("📌 시각화는 예시 수치 기반이며, 향후 실제 통계 데이터와 연동될 예정입니다.")
