import streamlit as st
import requests, os
from dotenv import load_dotenv

load_dotenv()
BACKEND_URL = os.getenv('BACKEND_URL','http://localhost:8000')

st.set_page_config(page_title='AI Career Copilot', layout='wide')
st.title('AI Career Copilot')

with st.sidebar:
    st.markdown('## Upload')
    uploaded_resume = st.file_uploader('Resume (PDF / DOCX / TXT)')
    uploaded_jd = st.file_uploader('Job description (optional)')

if uploaded_resume:
    files = {'file': (uploaded_resume.name, uploaded_resume.getvalue(), uploaded_resume.type)}
    r = requests.post(f"{BACKEND_URL}/upload_resume_file", files=files)
    if r.status_code == 200:
        resume_text = r.json()['text']
        st.subheader('Parsed resume')
        st.text_area('Resume text', resume_text, height=300)

        jd_text = None
        if uploaded_jd:
            jd_text = uploaded_jd.getvalue().decode('utf-8', errors='ignore')
            st.subheader('Job description')
            st.text_area('JD', jd_text, height=200)

        if st.button('Analyze for this JD' if jd_text else 'Analyze resume'):
            payload = {'resume_text': resume_text}
            if jd_text:
                payload['job_description'] = jd_text
            r2 = requests.post(f"{BACKEND_URL}/analyze_resume", json=payload)
            if r2.status_code == 200:
                res = r2.json()
                st.subheader('LLM Feedback')
                st.code(res.get('llm_feedback','(no feedback)'))
                st.write('Additional data:')
                st.json({k:v for k,v in res.items() if k!='llm_feedback'})
            else:
                st.error(f"Analysis failed: {r2.text}")
    else:
        st.error(f"Upload failed: {r.text}")
