# app.py
import streamlit as st

st.set_page_config(page_title="베스킨라빈스 키오스크 🍨", page_icon="🍦", layout="centered")

st.title("🍦 베스킨라빈스 키오스크에 오신 걸 환영해요! ✨")
st.write("마음 편하게 주문해보세요 😊 제가 하나씩 안내해드릴게요!")

# ---------------------------------------------
# 1) 실제 베스킨라빈스 용기 / 가격 / 스쿱 수
# ---------------------------------------------
containers = {
    "싱글레귤러": {"max_scoops": 1, "price": 3200},
    "더블주니어": {"max_scoops": 2, "price": 6200},
    "파인트": {"max_scoops": 4, "price": 9800},
    "쿼터": {"max_scoops": 4, "price": 18900},
    "패밀리": {"max_scoops": 5, "price": 23900},
    "하프갤런": {"max_scoops": 6, "price": 28900},
}

# ---------------------------------------------
# 2) 실제 베라 인기맛 리스트
# ---------------------------------------------
flavors_list = [
    "엄마는 외계인", "슈팅스타", "민트 초코", "뉴욕 치즈케이크",
    "체리쥬빌레", "바람과 함께 사라지다", "바닐라", "초콜릿",
    "쿠키앤크림", "아몬드 봉봉", "초코나무 숲", "요거트",
    "사랑에 빠진 딸기", "피스타치오 아몬드"
]

# ---------------------------------------------
# 3) 식사 방식
# ---------------------------------------------
st.header("1) 어디서 드시나요? 🍽️")
dine_choice = st.radio("선택해주세요!", ["매장에서 먹고 가기 🪑", "포장해가기 🛍️"])

# ---------------------------------------------
# 4) 용기 선택
# ---------------------------------------------
st.header("2) 용기를 선택해주세요 📦")
container = st.selectbox("원하는 사이즈를 골라주세요!", list(containers.keys()))

max_scoops = containers[container]["max_scoops"]
st.caption(f"👉 {container} 는 최대 **{max_scoops} 스쿱**을 선택할 수 있어요.")

# ---------------------------------------------
# 5) 스쿱 수 & 맛 선택
# ---------------------------------------------
st.header("3) 아이스크림 맛 선택 🍨")
scoops = st.slider("스쿱 수를 선택하세요", 1, max_scoops, value=max_scoops)

selected_flavors = st.multiselect(
    f"맛을 골라주세요 (최대 {scoops}개)",
    options=flavors_list
)

# 스쿱 수보다 많이 선택하면 에러
if len(selected_flavors) > scoops:
    st.error(f"⚠️ 스쿱 수는 {scoops}개인데 {len(selected_flavors)}개를 선택하셨어요!")
    st.stop()

# ---------------------------------------------
# 6) 토핑 (선택)
# ---------------------------------------------
toppings = {
    "초코시럽 🍫": 500,
    "스프링클 🌈": 300,
    "견과류 🥜": 700,
}

st.header("4) 토핑 추가하기 (선택)")
selected_toppings = st.multiselect("원하시는 토핑을 골라주세요!", list(toppings.keys()))
topping_price = sum(toppings[t] for t in selected_toppings)

# ---------------------------------------------
# 7) 가격 계산
# ---------------------------------------------
base_price = containers[container]["price"]
total_price = base_price + topping_price

# ---------------------------------------------
# 8) 결제
# ---------------------------------------------
st.markdown("---")
st.header("5) 결제 방법 선택 💳")

payment = st.radio("결제 수단을 선택해주세요!", ["현금 💵", "카드 💳", "기프티콘 🎟️"])

if payment == "기프티콘 🎟️":
    gifty_input = st.text_input("기프티콘 번호를 입력해주세요 (숫자 16자리)")

# ---------------------------------------------
# 9) 주문 요약
# ---------------------------------------------
st.subheader("📋 주문 요약")
st.write(f"- 식사 방식: **{dine_choice}**")
st.write(f"- 용기: **{container}**")
st.write(f"- 스쿱: **{scoops}개**")
st.write(f"- 맛: **{', '.join(selected_flavors) if selected_flavors else '아직 선택 안함'}**")
st.write(f"- 토핑: **{', '.join(selected_toppings) if selected_toppings else '없음'}**")
st.write(f"- 결제 방식: **{payment}**")

st.markdown(f"### 💰 총 결제 금액: **{total_price:,}원**")

# ---------------------------------------------
# 10) 주문 확정
# ---------------------------------------------
if st.button("✨ 주문 확정하기 ✨"):
    if not selected_flavors:
        st.warning("🍦 맛을 선택해야 주문할 수 있어요!")
    else:
        if payment == "기프티콘 🎟️" and (gifty_input.strip() == "" or len(gifty_input) < 16):
            st.error("⚠️ 기프티콘 번호가 올바르지 않아요!")
            st.stop()

        st.success("주문이 완료되었어요! 감사합니다 😊")
        st.balloons()

        st.write("주문 상세 내역👇")
        st.write(f"- {container} / {scoops} 스쿱")
        st.write(f"- 맛: {', '.join(selected_flavors)}")
        if selected_toppings:
            st.write(f"- 토핑: {', '.join(selected_toppings)}")
        st.write(f"- 결제 방식: {payment}")
        st.write(f"- 총액: **{total_price:,}원**")

        if dine_choice.startswith("매장"):
            st.info("🪑 매장에서 즐겁게 드시고 가세요!")
        else:
            st.info("🛍️ 포장 준비 중입니다. 잠시만 기다려주세요!")

st.markdown("---")
st.caption("※ 이 키오스크는 학습 및 시연용이며 실제 결제는 진행되지 않아요.")
