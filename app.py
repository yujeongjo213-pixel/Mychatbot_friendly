# app.py
import streamlit as st
from PIL import Image
import openai
import os

# ---------------------------
# 환경 변수에서 OpenAI API Key 불러오기
# Streamlit Cloud에서는 Secrets Manager에 OPENAI_API_KEY를 등록
openai.api_key = os.getenv("OPENAI_API_KEY")

# ---------------------------
# 페이지 설정
st.set_page_config(
    page_title="여행추천 챗봇",
    page_icon="🗺️",
    layout="wide"
)

# ---------------------------
# 사이드바 로고 및 안내
with st.sidebar:
    try:
        img = Image.open("Fitlab.png")  # 프로젝트 폴더 안에 있는 파일
        st.image(img, caption="Fitlab", use_container_width=True)
    except:
        st.markdown("Fitlab 로고 없음")
    st.markdown("## 여행추천 챗봇")
    st.markdown("---")
    st.markdown("친구처럼 친근하게 여행지를 추천해주는 챗봇이에요!")

# ---------------------------
# 세션 상태: 대화 저장
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": """
        너는 사용자가 여행지를 물어보면, 친구처럼 친근하고 재밌게 추천해주는 챗봇이야.
        답변은 부드럽고 유머러스하게 하며, 필요하면 소소한 여행 팁도 함께 알려줘.
        대답할 때는 '친구처럼 말하듯' 반말로 자연스럽게, 딱딱하지 않게 해줘. 이모지는 사용하지 않음.
        """}
    ]

# ---------------------------
# 사용자 입력
st.markdown("### 어디로 떠나실 건가요?")
user_input = st.text_input("무엇이든 물어보세요:", key="chat_input")

if st.button("보내기", key="send") and user_input:
    # 사용자 메시지 세션에 추가
    st.session_state.messages.append({"role": "user", "content": user_input})

    # OpenAI Chat Completions 호출 (최신 API)
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages
        )
        reply = response.choices[0].message.content

        # 챗봇 메시지 세션에 추가
        st.session_state.messages.append({"role": "assistant", "content": reply})
    except Exception as e:
        st.error(f"챗봇 응답 에러: {e}")

# ---------------------------
# 대화 출력
for msg in st.session_state.messages[1:]:  # 시스템 메시지는 제외
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"**친구:** {msg['content']}")
