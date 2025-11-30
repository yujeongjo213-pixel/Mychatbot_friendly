import streamlit as st
from PIL import Image
import openai

# --- 페이지 설정 ---
st.set_page_config(page_title="여행추천 챗봇", page_icon="🗺️", layout="wide")

# --- 사이드바 로고 ---
with st.sidebar:
    img = Image.open("Fitlab.png")
    st.image(img, caption="Fitlab", use_column_width=True)
    st.markdown("## 여행추천 챗봇")
    st.markdown("---")

# --- 이메일 입력 ---
if "started" not in st.session_state:
    st.session_state.started = False
if "email" not in st.session_state:
    st.session_state.email = ""

if not st.session_state.started:
    st.title("여행추천 챗봇에 오신 걸 환영해!")
    st.session_state.email = st.text_input("이메일을 입력해주세요:")
    if st.button("시작"):
        if st.session_state.email:
            st.session_state.started = True
        else:
            st.warning("이메일을 입력해야 시작할 수 있어요!")

# --- 세션 상태: 대화 저장 ---
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": """
        너는 사용자가 여행지를 물어보면, 친구처럼 친근하고 재밌게 추천해주는 챗봇이야.
        답변은 부드럽고 유머러스하게 하며, 필요하면 소소한 여행 팁도 함께 알려줘.
        대답할 때는 '친구처럼 말하듯' 반말로 자연스럽게, 딱딱하지 않게 해줘. 이모지는 없이.
        """}
    ]

# --- 챗봇 화면 ---
if st.session_state.started:
    st.markdown(f"### 안녕! {st.session_state.email}님, 여행지 추천해줄게 🙂")

    user_input = st.text_input("질문을 입력하세요:", key="chat_input")
    
    if st.button("전송", key="send"):
        if user_input:
            # 사용자 메시지 세션에 저장
            st.session_state["messages"].append({"role": "user", "content": user_input})

            # OpenAI API 호출 (예시)
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=st.session_state["messages"]
                )
                reply = response.choices[0].message.content
            except Exception as e:
                reply = f"챗봇 응답 에러: {e}"

            # 챗봇 메시지 세션에 저장
            st.session_state["messages"].append({"role": "assistant", "content": reply})

            # 화면에 표시
            st.text_area("챗봇:", value=reply, height=150)
