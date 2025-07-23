import streamlit as st
from translateGraph import langgraph_flow

st.title("다국어 자막 번역 챗봇")

# 앱을 한 번만 컴파일하여 저장 (캐시나 전역변수 활용 가능)
if "app" not in st.session_state:
    st.session_state.app = langgraph_flow.compile()

# 사용자 입력 컴포넌트
user_input = st.text_area("번역할 내용을 입력하세요")
target_language = st.text_input("목표 언어를 입력하세요 (예: 영어, 일본어, 스페인어 등)")
program_info = st.text_input("프로그램 정보를 입력하세요 (선택, 예: 방송 유형, 장르 등)")
people_info = st.text_input("인물 정보를 입력하세요 (선택, 예: 나이, 성별, 특징 등)")

chatbot_response = ""
chatbot_full_log = ""

if st.button("번역 및 스타일 조정 요청"):
    if user_input and target_language:
        program_info_val = program_info if program_info else "없음"
        people_info_val = people_info if people_info else "없음"
        # 그래프 실행을 위한 상태 입력
        state = {
            "input_text": user_input,
            "target_language": target_language,
            "program_info": program_info_val,
            "people_info": people_info_val,
            "subtitle": "",
            "translated": "",
            "styled": "",
            "quality_passed": "",
            "feedback": "",
            "fullLog": "",
        }
        result_state = st.session_state.app.invoke(state)
        # 최종 결과 styled 값 노출
        chatbot_response = result_state.get("styled", "번역 결과가 없습니다.")
        chatbot_full_log = result_state.get("fullLog", "전체 로그가 없습니다.")

    elif not user_input:
        st.warning("번역할 내용을 입력하세요.")
    elif not target_language:
        st.warning("목표 언어를 입력하세요.")

st.write("---")
if chatbot_response:
    st.write(chatbot_response)
else:
    st.write("챗봇 응답 영역")

st.write("---")
if chatbot_full_log:
    st.write(chatbot_full_log)
else:
    st.write("Langgraph Full Log")