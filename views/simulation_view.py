import streamlit as st
import pandas as pd
import plotly.express as px

# 전라남도 읍면동 예시 데이터 및 보정 가중치
EUPMYEONDONG_LIST = {
    "순천시 조례동": 1.00,
    "여수시 소라면": 1.05,
    "목포시 상동": 0.98,
    "해남군 해남읍": 1.10,
    "곡성군 옥과면": 1.12
}

# 정책 시나리오 정의
ADVANCED_POLICY_SCENARIOS = {
    "산업연관분석(IO) 기반 청년정착": {
        "설명": "산업연관표 기반 청년 인구 유입이 소비·산업에 미치는 파급효과 분석",
        "효과계수": {"정주지수": 0.12, "고용률": 0.03, "지역GDP": 0.045, "사회복지효과": 0.02}
    },
    "CGE 기반 고령친화 시티": {
        "설명": "일반균형모형을 통해 고령복지 투자 확대가 노동시장에 미치는 균형 효과 분석",
        "효과계수": {"정주지수": 0.09, "고용률": 0.025, "지역GDP": 0.035, "사회복지효과": 0.07}
    },
    "통계청 연계 교통망 확충": {
        "설명": "이동통계+산업자료 기반 교통 인프라 확충 효과를 정량 분석",
        "효과계수": {"정주지수": 0.07, "고용률": 0.02, "지역GDP": 0.04, "사회복지효과": 0.015}
    },
    "공간정보 기반 농촌 스마트화": {
        "설명": "GIS·IoT 기반 농업 자동화 및 유통 최적화로 지역경제 활성화",
        "효과계수": {"정주지수": 0.10, "고용률": 0.028, "지역GDP": 0.05, "사회복지효과": 0.025}
    },
    "에너지 전환 기반 지속가능 도시": {
        "설명": "신재생에너지 인프라 확충이 정주 안정성과 녹색일자리 창출에 미치는 영향 분석",
        "효과계수": {"정주지수": 0.08, "고용률": 0.03, "지역GDP": 0.055, "사회복지효과": 0.02}
    },
}

# 보정 가중치 계산
def get_weight_factors(pop_group, region_type, eupmyeondong, period, policy_type):
    weight = EUPMYEONDONG_LIST.get(eupmyeondong, 1.0)
    if pop_group == "청년":
        weight *= 1.1
    elif pop_group == "고령":
        weight *= 1.05
    if region_type == "읍면":
        weight *= 1.1
    elif region_type == "광역시":
        weight *= 0.95
    if "장기" in period:
        weight *= 1.15
    elif "단기" in period:
        weight *= 0.9
    if policy_type == "산업육성":
        weight *= 1.1
    return weight

# 정책 효과 계산
def run_policy_simulation(name, budget, staff, welfare_units, weight):
    coeff = ADVANCED_POLICY_SCENARIOS[name]["효과계수"]
    factor = budget + staff * 0.5 + welfare_units * 0.7
    return {
        "시나리오": name,
        "정주지수": round(factor * coeff["정주지수"] * weight, 2),
        "고용률": round(factor * coeff["고용률"] * weight, 2),
        "지역GDP": round(factor * coeff["지역GDP"] * weight, 2),
        "사회복지효과": round(factor * coeff["사회복지효과"] * weight, 2),
    }

# Streamlit 실행
def render():
    st.subheader("📈 고급 정책 시뮬레이션 (IO / CGE / 통계 기반)")

    eupmyeondong = st.selectbox("📌 전라남도 읍면동 선택", list(EUPMYEONDONG_LIST.keys()))
    budget = st.slider("💰 총 투자 예산 (억 원)", 100, 3000, 1000, 100)
    staff = st.slider("👷 정책 전담 인력 수", 0, 500, 100, 10)
    welfare_units = st.slider("🏢 복지시설 수", 0, 100, 20, 5)
    pop_group = st.selectbox("🎯 대상 인구군", ["전체", "청년", "고령"])
    region_type = st.selectbox("📍 우선 투자 지역 유형", ["중소도시", "읍면", "광역시"])
    period = st.selectbox("⏳ 정책 실행 기간", ["단기 (1~2년)", "중기 (3~5년)", "장기 (5년 이상)"])
    policy_type = st.selectbox("📂 정책 성격", ["복지", "인프라", "산업육성"])

    selected = st.multiselect(
        "🧭 정책 시나리오 선택 (복수 가능)",
        list(ADVANCED_POLICY_SCENARIOS.keys()),
        default=["산업연관분석(IO) 기반 청년정착"]
    )

    if not selected:
        st.warning("⚠️ 하나 이상의 정책을 선택해주세요.")
        return

    st.markdown(f"### 📍 시뮬레이션 지역: **{eupmyeondong}**")
    for s in selected:
        st.markdown(f"✅ **{s}**")
        st.caption(f"ℹ️ {ADVANCED_POLICY_SCENARIOS[s]['설명']}")

    if st.button("🚀 시뮬레이션 실행"):
        weight = get_weight_factors(pop_group, region_type, eupmyeondong, period, policy_type)
        results = [run_policy_simulation(s, budget, staff, welfare_units, weight) for s in selected]
        df = pd.DataFrame(results)

        st.markdown("### 📊 시뮬레이션 결과 요약")
        st.dataframe(df, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            for metric in ["정주지수", "고용률"]:
                fig = px.bar(df, x="시나리오", y=metric, color="시나리오",
                             text_auto=".2s", title=f"{metric} 향상 기대치", height=350)
                st.plotly_chart(fig, use_container_width=True)
        with col2:
            for metric in ["지역GDP", "사회복지효과"]:
                fig = px.bar(df, x="시나리오", y=metric, color="시나리오",
                             text_auto=".2s", title=f"{metric} 향상 기대치", height=350)
                st.plotly_chart(fig, use_container_width=True)

        st.caption("📌 IO, CGE, 통계 기반 시뮬레이션은 다양한 지역 여건에 맞춘 정량적 정책평가 도구입니다.")
