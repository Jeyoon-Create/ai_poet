from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
import os

st.title('시인 앱')

# API 키 입력 섹션
st.markdown('## API 키 설정')
api_key = st.text_input(
    'OpenAI API 키를 입력하세요',
    type='password',
    placeholder='sk-...',
    help='OpenAI API 키는 https://platform.openai.com/api-keys 에서 발급받을 수 있습니다.'
)

if api_key:
    # API 키를 환경 변수로 설정
    os.environ['OPENAI_API_KEY'] = api_key
    
    # 모델 초기화
    try:
        openai = init_chat_model(
            'gpt-3.5-turbo',
            temperature=0.7
        )
        
        # 프롬프트 설정
        prompt = ChatPromptTemplate.from_messages([
            ('system', '당신은 창의적인 시(poet) 작가입니다.\n'),
            ('user', '{input}\n')
        ])
        
        chain = prompt | openai | StrOutputParser()
        
        st.success('✅ API 키가 성공적으로 설정되었습니다!')
        
        # 시 주제 입력 섹션
        st.markdown('---')
        st.markdown('## 시 주제', unsafe_allow_html=True)
        
        content = st.text_input('', placeholder='시의 주제를 입력하세요.')
        
        if content:
            with st.spinner('주제를 읽고 있습니다...'):
                st.markdown(
                    '<span style="font-size:20px;">입력한 시의 주제는 ' +
                    '<span style="font-size:20px; background-color: #defae0;">' + 
                    content + '</span>입니다.</span>',
                    unsafe_allow_html=True
                )
        
        # 시 생성 버튼
        if st.button('시 만들기 요청'):
            if not content:
                st.warning('⚠️ 시의 주제를 먼저 입력해주세요.')
            else:
                with st.spinner('시를 생성하는 중입니다... 잠시만 기다려주세요!'):
                    try:
                        result = chain.invoke({
                            'input': f'{content}에 대한 시(poet)를 창작해줘.'
                        })
                        st.markdown('### 생성된 시')
                        st.markdown(result)
                    except Exception as e:
                        st.error(f'❌ 오류가 발생했습니다: {e}')
    
    except Exception as e:
        st.error(f'❌ API 키 설정 중 오류가 발생했습니다: {e}')
        st.info('API 키를 확인하고 다시 입력해주세요.')

else:
    st.info('👆 OpenAI API 키를 입력하면 시작할 수 있습니다.')
    st.markdown('''
    ### 사용 방법
    1. OpenAI API 키를 위 입력란에 입력하세요
    2. 시의 주제를 입력하세요
    3. "시 만들기 요청" 버튼을 클릭하세요
    
    **API 키 발급 방법:**
    - [OpenAI Platform](https://platform.openai.com/api-keys)에서 로그인
    - "Create new secret key" 버튼 클릭
    - 생성된 키를 복사하여 위 입력란에 붙여넣기
    ''')