import streamlit as st
import time
from rag.rag_main import init_rag, ask_question

st.set_page_config(page_title="소득세 챗봇", page_icon="🤖")
st.title("🤖 소득세 챗봇")
st.caption("소득세에 관련된 모든 것을 답해드립니다!")

@st.cache_resource
def load_rag_chain():
    return init_rag()

qa_chain = load_rag_chain()

if "message_list" not in st.session_state:
    st.session_state.message_list = []

# 이전 메시지 출력
for message in st.session_state.message_list:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 유저 입력창
user_question = st.chat_input("소득세에 관련된 궁금한 내용을 말씀해주세요!")

if user_question:
    # 유저 메시지 출력
    with st.chat_message("user"):
        st.write(user_question)
    st.session_state.message_list.append({"role": "user", "content": user_question})

    # AI 답변 스트리밍 처리
    with st.chat_message("ai"):
        message_placeholder = st.empty()
        ai_answer = ""

        # 실제 답변 가져오기
        result = ask_question(qa_chain, user_question)
        full_answer = result["answer"]

        # 한 글자씩 스트리밍
        for char in full_answer:
            ai_answer += char
            message_placeholder.write(ai_answer)
            time.sleep(0.01)  # 속도 조절 가능

        # 출처(expander)
        with st.expander("출처 보기"):
            for src in result.get("sources", []):
                st.write(f"{src['source']} ---- {src['content']}")

    st.session_state.message_list.append({"role": "ai", "content": full_answer})
