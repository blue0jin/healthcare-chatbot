import streamlit as st
from openai import OpenAI

# 페이지 설정
st.set_page_config(
    page_title="🏥 헬스케어 AI",
    page_icon="🏥",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 커스텀 CSS - 깔끔하고 심플한 디자인
st.markdown("""
<style>
    /* 전체 배경 */
    .stApp {
        background-color: #ffffff;
    }
    
    /* 메인 컨테이너 */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 700px;
    }
    
    /* 제목 스타일 */
    .main-title {
        text-align: center;
        color: #2c3e50;
        font-size: 2.2rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        padding: 1rem 0;
    }
    
    .subtitle {
        text-align: center;
        color: #7f8c8d;
        font-size: 1rem;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* API 키 입력 영역 */
    .api-container {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e9ecef;
        margin-bottom: 2rem;
    }
    
    /* 채팅 메시지 스타일 */
    .user-message {
        background: #3498db;
        color: white;
        padding: 0.8rem 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        margin-left: 2rem;
        border-bottom-right-radius: 4px;
    }
    
    .bot-message {
        background: #f8f9fa;
        color: #2c3e50;
        padding: 0.8rem 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        margin-right: 2rem;
        border: 1px solid #e9ecef;
        border-bottom-left-radius: 4px;
    }
    
    /* 입력 필드 스타일 */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 2px solid #e9ecef;
        padding: 0.5rem;
        font-size: 1rem;
        font-weight: bold;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3498db;
        box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.1);
    }
    
    /* 버튼 스타일 */
    .stButton > button {
        background: #3498db;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: 500;
        transition: background-color 0.2s;
    }
    
    .stButton > button:hover {
        background: #2980b9;
    }
    
    /* 경고 메시지 */
    .stAlert {
        border-radius: 8px;
    }
    
    /* 사이드바 숨김 */
    .css-1d391kg {
        display: none;
    }
    
    /* 추천 질문 버튼 */
    .suggestion-btn {
        background: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 8px;
        padding: 0.7rem;
        margin: 0.3rem;
        cursor: pointer;
        transition: all 0.2s;
        color: #495057;
        font-size: 0.9rem;
    }
    
    .suggestion-btn:hover {
        border-color: #3498db;
        background: white;
    }
</style>
""", unsafe_allow_html=True)

# 메인 제목
st.markdown('<h1 class="main-title">🏥 건강 궁금해요? 궁금하면 물어봐!</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">건강에 관한 궁금증을 해결해드립니다</p>', unsafe_allow_html=True)

# Streamlit app
st.title("여행용 챗봇과 대화하기")
openai_api_key = st.secrets['openai']['API_KEY']
client = OpenAI(api_key  = openai_api_key)

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [  
        {"role": "system", 
         "content": "한국어로 기본 제공하고 사용자에게 다른 나라 언어로도 답변 필요한지 꼭 물어봐줘."
          "당신은 헬스케어에 관한 질문에 답하는 챗봇입니다. "
          "만약에 헬스케어, 건강 관련 외에 질문에 대해서는 답변하지 마세요."
          "너가 잘 모르는 내용은 만들어서 답변하지 마렴. 환각증세를 철저하게 없애 주세요."
          "증상에 대한 관련 병명, 진단, 관련병원진료과, 치료법, 예방법, 식생활, 운동 등 다양한 주제에 대해 친절하게 안내하는 챗봇입니다."
        }  
    ]

# 추천 질문
if len(st.session_state.messages) == 1:  # 시스템 메시지만 있을 때
    st.markdown("**💡 추천 질문**")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🤕 두통 원인과 해결법", key="q1"):
            st.session_state.user_question = "두통이 자주 발생하는데 원인과 해결법을 알려주세요"
        if st.button("🍎 건강한 식단 조언", key="q2"):
            st.session_state.user_question = "건강한 식단을 위한 조언을 해주세요"
    
    with col2:
        if st.button("🏃‍♂️ 운동 추천", key="q3"):
            st.session_state.user_question = "운동을 시작하려는데 어떤 운동이 좋을까요?"
        if st.button("😌 스트레스 관리", key="q4"):
            st.session_state.user_question = "스트레스 관리 방법을 알려주세요"

# 사용자 입력
st.markdown("---")
user_input = st.text_input("💬 건강에 관한 질문을 입력하세요", key="user_input", placeholder="예: 감기 예방법을 알려주세요")

# 추천 질문이 선택된 경우 처리
if hasattr(st.session_state, 'user_question'):
    user_input = st.session_state.user_question
    del st.session_state.user_question

# 메시지 전송 처리
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    send_button = st.button("📤 전송", use_container_width=True)

if (send_button and user_input) or user_input:
    if user_input:
        # 사용자 메시지 추가
        st.session_state.messages.append({"role": "user", "content": user_input})

        # OpenAI API 호출
        with st.spinner("🤔 답변을 생성하고 있습니다..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=st.session_state.messages,
                    temperature=0.7
                )
                
                # AI 응답 추가
                response_message = response.choices[0].message.content
                st.session_state.messages.append({"role": "assistant", "content": response_message})
                
            except Exception as e:
                st.error(f"❌ 오류가 발생했습니다: {str(e)}")

# 대화 내용 표시
if len(st.session_state.messages) > 1:
    st.markdown("---")
    st.markdown("**💭 대화 내용**")
    
    # 시스템 메시지 제외한 메시지들만 필터링
    user_messages = [msg for msg in st.session_state.messages if msg["role"] != "system"]
    
    # 최근 답변을 위쪽에 보이도록 역순으로 정렬
    user_messages.reverse()
    
    # 답변 표시 상태 관리
    if "show_answers" not in st.session_state:
        st.session_state.show_answers = {}
    
    for i, message in enumerate(user_messages):
        message_id = f"msg_{len(user_messages) - i - 1}"
        
        if message["role"] == "user":
            st.markdown(f'<div class="user-message">👤 <strong>나:</strong> {message["content"]}</div>', 
                       unsafe_allow_html=True)
        else:
            # 최근 질문-답변 쌍 (첫 번째와 두 번째)은 항상 보이기
            if i <= 1:  # 최근 질문과 답변
                st.markdown(f'<div class="bot-message">🤖 <strong>헬스케어 AI:</strong> {message["content"]}</div>', 
                           unsafe_allow_html=True)
            else:  # 과거 AI 답변들
                # 토글 버튼
                col1, col2 = st.columns([6, 1])
                with col1:
                    st.markdown('<div class="bot-message">🤖 <strong>헬스케어 AI:</strong> 답변이 있습니다</div>', 
                               unsafe_allow_html=True)
                with col2:
                    if message_id not in st.session_state.show_answers:
                        st.session_state.show_answers[message_id] = False
                    
                    if st.button("답변보기" if not st.session_state.show_answers[message_id] else "숨기기", 
                               key=f"toggle_{message_id}"):
                        st.session_state.show_answers[message_id] = not st.session_state.show_answers[message_id]
                        st.rerun()
                
                # 답변 내용 표시 (토글 상태에 따라)
                if st.session_state.show_answers.get(message_id, False):
                    st.markdown(f'<div class="bot-message" style="margin-top: 0.2rem;">📝 {message["content"]}</div>', 
                               unsafe_allow_html=True)

# 대화 초기화 버튼
if len(st.session_state.messages) > 1:
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🗑️ 대화 초기화", use_container_width=True):
            st.session_state.messages = st.session_state.messages[:1]  # 시스템 메시지만 유지
            st.rerun()

# 푸터
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d; font-size: 0.9rem; padding: 1rem;">
    ⚠️ 본 서비스는 참고용이며, 실제 의료 진단을 대체할 수 없습니다.<br>
    심각한 증상이 있으시면 반드시 전문의와 상담하세요.
</div>
""", unsafe_allow_html=True)
