import requests
import streamlit as st

from app.config import settings

st.title('RAG Chatbot')

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

api_url = (
    f'http://'
    f'{settings.streamlit.STREAMLIT_BACKEND_HOST}:'
    f'{settings.streamlit.STREAMLIT_BACKEND_PORT}'
    f'/api/rag/'
)

for msg in st.session_state['messages']:
    st.chat_message(msg['role']).write(msg['content'])

if prompt := st.chat_input('Ask something...'):
    st.session_state['messages'].append({'role': 'user', 'content': prompt})
    st.chat_message('user').write(prompt)
    with st.spinner('Thinking...'):
        try:
            response = requests.post(api_url, json={'question': prompt})
            response.raise_for_status()
            answer = response.json()['answer']
        except Exception as e:
            answer = f'Error: {e}'
    st.session_state['messages'].append({'role': 'assistant', 'content': answer})
    st.chat_message('assistant').write(answer)
