import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="World MBTI Dashboard", layout="wide")

# -------------------------
# 1. 데이터 로드
# -------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df

df = load_data()

st.title("🌍 국가별 MBTI 비율 대시보드 (Interactive Plotly Graph)")

# -------------------------
# 2. 국가 선택
# -------------------------
country_list = df["Country"].unique()
selected_country = st.selectbox("국가를 선택하세요:", country_list)

# -------------------------
# 3. 선택한 국가의 데이터 처리
# -------------------------
row = df[df["Country"] == selected_country].iloc[0]

mbti_types = df.columns[1:]   # Country 제외한 MBTI 항목
values = row[1:].values

data = pd.DataFrame({
    "MBTI": mbti_types,
    "Value": values
})

# 1등 찾기
max_value = data["Value"].max()

# -------------------------
# 4. 색상 설정
#    - 1등: 빨간색
#    - 나머지: 파랑→보라 계열 그라데이션
# -------------------------
colors = []
for v in data["Value"]:
    if v == max_value:
        colors.append("red")
    else:
        # 값 기반 그라데이션
        # 값이 낮을수록 밝은 파랑, 높을수록 진한 보라
        gradient = int(150 + v * 500)
        gradient = min(255, gradient)
        colors.append(f"rgb({gradient//3}, {gradient//2}, {gradient})")

# -------------------------
# 5. Plotly 그래프 생성
# -------------------------
fig = px.bar(
    data,
    x="MBTI",
    y="Value",
    title=f"{selected_country} - MBTI 비율",
)

fig.update_traces(marker_color=colors)

# y축 퍼센트 표시
fig.update_layout(
    yaxis=dict(tickformat=".1%"),
    title_font_size=24,
    xaxis_title="",
    yaxis_title="비율",
    template="plotly_white"
)

# -------------------------
# 6. 그래프 출력
# -------------------------
st.plotly_chart(fig, use_container_width=True)

st.markdown("Made with ❤️ using Streamlit + Plotly")
