# app.py
import streamlit as st

st.set_page_config(page_title="베스킨라빈스 키오스크 🍨", page_icon="🍦", layout="centered")

st.title("베스킨라빈스 키오스크에 오신 걸 환영해요! 🍨✨")
st.write("친절한 음성은 없지만, 제가 센스있게 도와드릴게요 😉")

# --- 데이터 정의 (용기별 최대 스쿱 및 가격) ---
containers = {
    "컵 (싱글)"         : {"max_scoops": 1, "price": 3000},
    "컵 (더블)"         : {"max_scoops": 2, "price": 5500},
    "콘 (싱글)"         : {"max_scoops": 1, "price": 3500},  # 콘은 컵보다 살짝 비쌈
    "콘 (더블)"         : {"max_scoops": 2, "price": 6000},
    "파인트 (473ml)"    : {"max_scoops": 4, "price": 12000},
}

# --- 용기별 선택 가능한 맛 (예시로 분류) ---
flavors_per_container = {
    "컵 (싱글)": ["바닐라", "초콜릿", "스트로베리", "민트초코"],
    "컵 (더블)": ["바닐라", "초콜릿", "스트로베리", "민트초코", "쿠키앤크림", "녹차"],
    "콘 (싱글)": ["바닐라", "초콜릿", "쿠키앤크림"],
    "콘 (더블)": ["바닐라", "초콜릿", "스트로베리", "민트초코", "쿠키앤크림"],
    "파인트 (473ml)": ["바닐라", "초콜릿", "스트로베리", "민트초코", "쿠키앤크림", "녹차", "피스타치오", "아몬드봉봉"],
}

# --- 사이드 옵션 (예: 토핑) 간단 추가 (선택사항) ---
toppings = {
    "초코시럽": 500,
    "견과류": 700,
    "스프링클": 300,
    "과일토핑": 800,
}

st.header("1) 식사 방식 선택 🍽️")
dine_choice = st.radio("매장에서 드실 건가요, 포장해서 가져가실 건가요?", ("매장 식사 (테이블)", "포장 (테이크아웃)"))

st.header("2) 용기(사이즈) 선택 📦")
container = st.selectbox("원하시는 용기를 골라주세요.", list(containers.keys()))

max_scoops = containers[container]["max_scoops"]
st.caption(f"이 용기는 최대 {max_scoops} 스쿱까지 선택할 수 있어요.")

st.header("3) 아이스크림 맛 선택 🍨")
available_flavors = flavors_per_container.get(container, [])
st.write("아래에서 원하는 맛을 골라주세요. (스쿱 수에 맞춰 골라야 해요)")

# 스쿱 수 선택
scoops = st.slider("스쿱 수를 선택하세요", min_value=1, max_value=max_scoops, value=1, step=1)

# 멀티셀렉트로 맛 선택 (선택 개수 유효성 검사)
selected_flavors = st.multiselect(f"맛을 선택하세요 (최대 {scoops}개)", options=available_flavors)

# 선택 검사
if len(selected_flavors) > scoops:
    st.error(f"❗ 스쿱 수보다 많은 맛을 고르셨어요. {scoops}개까지만 선택해주세요.")
    st.stop()

# 토핑 선택 (옵션)
st.header("추가 옵션 (선택)")
selected_toppings = st.multiselect("토핑을 추가하시겠어요? (유료)", options=list(toppings.keys()))
toppings_total = sum(toppings[t] for t in selected_toppings)

# --- 가격 계산 ---
base_price = containers[container]["price"]
# 가격 결정 방식: 용기별 고정 가격을 사용 (실제 매장과 다를 수 있음)
total_price = base_price + toppings_total

st.markdown("---")
st.header("4) 최종 주문 확인 및 결제 💳💵")

st.subheader("주문 요약")
st.write(f"- 식사 방식: **{dine_choice}**")
st.write(f"- 용기: **{container}**")
st.write(f"- 스쿱 수: **{scoops}**")
st.write(f"- 선택한 맛: **{', '.join(selected_flavors) if selected_flavors else '아직 선택 안함'}**")
if selected_toppings:
    st.write(f"- 토핑: **{', '.join(selected_toppings)}** (+{toppings_total}원)")
else:
    st.write(f"- 토핑: **없음**")

st.markdown(f"### 총액: **{total_price:,}원** 🎉")

# 결제 수단 선택
payment = st.radio("결제 방법을 골라주세요", ("현금 결제 💵", "카드 결제 💳"))
note = ""
if payment == "현금 결제 💵":
    note = "현금 결제 선택 시 거스름돈 준비해드려요. 😊"
else:
    note = "카드 결제는 IC/무선 단말기로 진행해 주세요. 안전하게 처리됩니다. 🔒"
st.caption(note)

# 주문자 이름(선택)
name = st.text_input("영수증에 적을 이름을 알려주세요 (선택)", "")

# 주문 완료 버튼
if st.button("주문 확정 🎯"):
    if not selected_flavors:
        st.warning("아직 맛을 선택하지 않으셨어요 — 맛을 골라야 주문할 수 있어요! 🍨")
    else:
        # 주문 요약 메시지
        st.success("주문이 완료되었어요! 감사합니다 🍦✨")
        st.write("아래 내용을 확인해 주세요 —")
        st.write(f"- 이름: **{name if name else '손님'}**")
        st.write(f"- {container} / {scoops} 스쿱")
        st.write(f"- 맛: {', '.join(selected_flavors)}")
        if selected_toppings:
            st.write(f"- 토핑: {', '.join(selected_toppings)}")
        st.write(f"- 결제: {payment}")
        st.markdown(f"**총 결제 금액: {total_price:,}원**")
        if dine_choice.startswith("매장"):
            st.info("안내: 매장 좌석으로 가져다 드릴게요. 잠시만 기다려 주세요 🪑")
        else:
            st.info("안내: 포장해서 준비해드릴게요. 곧 찾아가실 수 있어요 🛍️")
        st.balloons()
        st.write("원하시면 다른 주문을 시작하려면 페이지 상단으로 가서 다시 선택하세요. 또 올게요! 😄")

st.markdown("---")
st.caption("이 키오스크는 예시용이에요 — 실제 매장 시스템과는 다를 수 있어요. 결제는 시연용으로 처리되지 않습니다.")
