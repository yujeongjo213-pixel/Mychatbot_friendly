import streamlit as st
from PIL import Image
import openai

# 🔑 본인 OpenAI API 키

# 페이지 설정
st.set_page_config(
    page_title="여행추천 챗봇",
    page_icon="🗺️",
    layout="wide"
)

with st.sidebar:
    img = Image.open("Fitlab.png")  # 절대 경로 대신 파일명만
    st.sidebar.image(img, caption="Fitlab", use_column_width=True)
    st.markdown("## 여행추천 챗봇")
    st.markdown("---")

# 세션 상태: 대화 저장
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": """
        너는 사용자가 여행지를 물어보면, 친구처럼 친근하고 재밌게 추천해주는 챗봇이야.
        답변은 부드럽고 유머러스하게 하며, 필요하면 소소한 여행 팁도 함께 알려줘.
        대답할 때는 '친구처럼 말하듯' 반말로 자연스럽게, 딱딱하지 않게 해줘.
        """}
    ]

# 사용자 입력
user_input = st.text_input("질문을 입력하세요:", "")

if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    
    # OpenAI API 호출
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state["messages"]
    )
    answer = response.choices[0].message.content
    st.session_state["messages"].append({"role": "assistant", "content": answer})

# 대화창 스타일
chat_container_style = """
<style>
#chatbox {
    max-height: 500px;
    overflow-y: auto;
    padding: 10px;
    border: 1px solid #eee;
    border-radius: 10px;
    background-color: #FAFAFA;
}
</style>
"""
st.markdown(chat_container_style, unsafe_allow_html=True)

# 대화 출력
st.markdown('<div id="chatbox">', unsafe_allow_html=True)
for msg in st.session_state["messages"]:
    if msg["role"] == "system":
        continue  # 화면에 표시하지 않음
    if msg["role"] == "user":
        st.markdown(
            f"""
            <div style="display:flex; justify-content:flex-end; margin:5px 0;">
                <div style="
                    background-color:#DCF8C6;
                    padding:10px 15px;
                    border-radius:15px;
                    max-width:70%;
                    word-wrap:break-word;">
                    {msg['content']}
                </div>
            </div>
            """, unsafe_allow_html=True
        )
    else:  # assistant
        st.markdown(
            f"""
            <div style="display:flex; justify-content:flex-start; margin:5px 0;">
                <div style="
                    background-color:#F1F0F0;
                    padding:10px 15px;
                    border-radius:15px;
                    max-width:70%;
                    word-wrap:break-word;">
                    {msg['content']}
                </div>
            </div>
            """, unsafe_allow_html=True
        )
st.markdown('</div>', unsafe_allow_html=True)
