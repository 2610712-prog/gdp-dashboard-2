import streamlit as st

# 1. 페이지 설정 및 제목
st.set_page_config(page_title="디즈니/픽사 무비 스토어", page_icon="🎬", layout="centered")
st.title("🎬 디즈니/픽사 무비 스토어")
st.write("원하는 영화와 수량을 선택하신 후 결제하기 버튼을 눌러주세요.")
st.markdown("---")

# 2. 영화 및 가격 데이터 설정
movies = {
    "겨울왕국": {"price": 12000, "img": "❄️"},
    "인사이드 아웃": {"price": 14000, "img": "🧠"},
    "주토피아": {"price": 11000, "img": "🦊"},
    "코코": {"price": 13000, "img": "🎸"}
}

# 3. 세션 상태(Session State)를 이용해 장바구니 초기화
if "cart" not in st.session_state:
    st.session_state.cart = {}

# 4. 영화 목록 및 수량 선택 화면 (2x2 그리드 레이아웃)
st.subheader("🍿 판매 중인 영화 목록")
col1, col2 = st.columns(2)

for i, (title, info) in enumerate(movies.items()):
    # 열(Column) 번갈아가며 배치
    with col1 if i % 2 == 0 else col2:
        st.info(f"### {info['img']} {title}\n**가격: {info['price']:,}원**")
        
        # 영화별 수량 선택 (0이면 구매 안 함)
        count = st.number_input(f"'{title}' 구매 수량", min_value=0, max_value=10, value=0, key=f"num_{title}")
        
        # 수량이 0보다 크면 장바구니 세션에 저장, 0이면 제거
        if count > 0:
            st.session_state.cart[title] = count
        elif title in st.session_state.cart:
            del st.session_state.cart[title]

st.markdown("---")

# 5. 장바구니 및 결제 섹션
st.subheader("🛒 장바구니 현황")

if not st.session_state.cart:
    st.warning("장바구니가 비어 있습니다. 영화 수량을 선택해 주세요.")
else:
    total_price = 0
    # 장바구니 내역을 표(Table) 형태로 예쁘게 보여주기 위한 데이터 구성
    cart_data = []
    
    for title, count in st.session_state.cart.items():
        item_price = movies[title]["price"] * count
        total_price += item_price
        cart_data.append({
            "영화 제목": title,
            "수량": f"{count}편",
            "금액": f"{item_price:,}원"
        })
    
    # 표 출력
    st.table(cart_data)
    
    # 총 결제 금액 표시
    st.metric(label="총 결제 금액", value=f"{total_price:,}원")
    
    # 결제 버튼
    if st.button("💳 최종 결제하기", type="primary"):
        st.balloons() # 축하 풍선 효과 🎉
        st.success(f"🎉 성공적으로 결제가 완료되었습니다! 총 {total_price:,}원이 결제되었습니다.")
        # 결제 후 장바구니 비우기 원할 시 주석 해제
        # st.session_state.cart.clear()