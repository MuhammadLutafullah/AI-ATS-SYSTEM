import streamlit as st
import os
import PyPDF2
import requests
import json

# ========== PAGE CONFIGURATION ==========
st.set_page_config(
    page_title="AI ATS System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ========== FIX: CLOUD + LOCAL API KEY LOAD ==========
try:
    # Cloud deployment ke liye (Streamlit Secrets)
    OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
    st.success("✅ Using API key from Streamlit Secrets (Cloud Mode)")
except Exception:
    # Local development ke liye (.env file)
    from dotenv import load_dotenv
    load_dotenv()
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    st.info("💻 Using API key from .env file (Local Mode)")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# ========== CUSTOM CSS ==========
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    * {
        font-family: 'Inter', sans-serif;
    }

    /* Fix white background issue */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }

    /* Main container */
    .main {
        background: transparent;
    }

    /* Hero Section */
    .hero {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 1.5rem;
        margin-bottom: 2rem;
        text-align: center;
        animation: fadeIn 0.8s ease;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }

    .hero h1 {
        font-size: 2.5rem;
        margin: 0;
        color: white;
        font-weight: 700;
    }

    .hero p {
        color: #e0e0e0;
        margin-top: 0.5rem;
        font-size: 1.1rem;
    }

    /* Card styling */
    .custom-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 1.5rem;
        border-radius: 1rem;
        margin-bottom: 1rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .custom-card:hover {
        transform: translateY(-5px);
        background: rgba(255, 255, 255, 0.15);
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    }

    .custom-card h3 {
        color: white;
        margin: 0 0 1rem 0;
    }

    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.6rem 1.5rem;
        border-radius: 0.5rem;
        font-weight: 500;
        font-size: 0.9rem;
        transition: all 0.3s ease;
        width: 100%;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.5);
    }

    /* Text area styling */
    .stTextArea label {
        color: white !important;
        font-weight: 500 !important;
    }

    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 0.75rem;
        color: white !important;
        transition: all 0.3s ease;
    }

    .stTextArea textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.3);
        background: rgba(255, 255, 255, 0.15);
    }

    .stTextArea textarea::placeholder {
        color: rgba(255, 255, 255, 0.5);
    }

    /* File uploader styling */
    .stFileUploader {
        background: transparent;
    }

    .stFileUploader > div {
        background: rgba(255, 255, 255, 0.1);
        border: 2px dashed #667eea;
        border-radius: 1rem;
        color: white;
    }

    .stFileUploader label {
        color: white !important;
    }

    /* Success message */
    .stSuccess {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        border-radius: 0.75rem;
        padding: 0.75rem;
        animation: slideIn 0.5s ease;
    }

    /* Warning message */
    .stWarning {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
        border-radius: 0.75rem;
        padding: 0.75rem;
    }

    /* Response box */
    .response-box {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 1rem;
        padding: 1.5rem;
        margin: 1rem 0;
        color: #e0e0e0;
        border-left: 4px solid #667eea;
        animation: fadeIn 0.5s ease;
    }

    /* Divider */
    .custom-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #667eea, #764ba2, transparent);
        margin: 1rem 0;
    }

    /* Section title */
    .section-title {
        color: white;
        font-size: 1.2rem;
        font-weight: 600;
        margin: 1rem 0;
    }

    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }

    /* Fix label colors */
    .stMarkdown p {
        color: white;
    }

    /* Caption styling */
    .stCaption {
        color: rgba(255, 255, 255, 0.7) !important;
    }

    /* Spinner color */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }
</style>
""", unsafe_allow_html=True)

# ========== HEADER SECTION ==========
st.markdown("""
<div class="hero">
    <h1>🤖 AI-Powered ATS System</h1>
    <p>Intelligent Resume Screening & Job Matching</p>
</div>
""", unsafe_allow_html=True)

# ========== MAIN CONTENT ==========
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("""
    <div class="custom-card">
        <h3>📝 Job Description</h3>
    </div>
    """, unsafe_allow_html=True)
    txt_input = st.text_area("", placeholder="Paste the job description here...", height=250,
                             label_visibility="collapsed")

with col2:
    st.markdown("""
    <div class="custom-card">
        <h3>📄 Upload Resume / CV</h3>
    </div>
    """, unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=['pdf'], label_visibility="collapsed", help="Upload PDF file only")

    if uploaded_file is not None:
        st.success("✅ PDF Uploaded Successfully!")

# ========== DIVIDER ==========
st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# ========== BUTTON SECTION ==========
st.markdown('<p class="section-title">🔍 Analysis Options</p>', unsafe_allow_html=True)

btn_col1, btn_col2, btn_col3, btn_col4 = st.columns(4)


# ========== FUNCTIONS ==========
def extract_text_from_pdf(uploaded_file):
    if uploaded_file is not None:
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ''
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
        return text
    else:
        raise FileNotFoundError("No file uploaded")


def get_llm_response(job_description, cv_content, prompt):
    full_prompt = f"""
Job Description:
{job_description}

Resume/CV:
{cv_content}

Instruction:
{prompt}
"""
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://ai-ats-system.streamlit.app",
        "X-Title": "ATS System"
    }
    payload = {
        "model": "meta-llama/llama-3-8b-instruct",
        "messages": [{"role": "user", "content": full_prompt}],
        "temperature": 0.7,
        "max_tokens": 1000
    }
    try:
        response = requests.post(OPENROUTER_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {str(e)}\n\nPlease check your API key or try again later."


# ========== PROMPTS ==========
input_prompt1 = """
You are an experienced Technical Human Resource Manager, your task is to review the provided resume against the job description. 
Please share your professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2 = """
You are an Technical Human Resource Manager with expertise in data science, 
your role is to scrutinize the resume in light of the job description provided. 
Share your insights on the candidate's suitability for the role from an HR perspective. 
Additionally, offer advice on enhancing the candidate's skills and identify areas where improvement is needed.
"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. As a Human Resource manager,
assess the compatibility of the resume with the role. Give me what are the keywords that are missing
Also, provide recommendations for enhancing the candidate's skills and identify which areas require further development.
"""

input_prompt4 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. 
Your task is to evaluate the resume against the provided job description. Give me the percentage match of the resume to the job description. 
First, provide the percentage in numbers, then list the missing keywords, and finally provide your thoughts.
"""

with btn_col1:
    submit1 = st.button("📊 Tell Me About Resume", use_container_width=True)

with btn_col2:
    submit4 = st.button("🎯 Percentage Match", use_container_width=True)

with btn_col3:
    submit3 = st.button("🔑 Missing Keywords", use_container_width=True)

with btn_col4:
    submit2 = st.button("💡 Improvise Skills", use_container_width=True)

# ========== RESPONSE SECTION ==========
if submit1:
    if uploaded_file is not None:
        with st.spinner("🔍 Analyzing resume..."):
            file_content = extract_text_from_pdf(uploaded_file)
            response = get_llm_response(txt_input, file_content, input_prompt1)
            st.markdown(f"""
            <div class="response-box">
                <h4 style="color: white; margin: 0 0 0.5rem 0;">📊 Analysis Result</h4>
                <div class="custom-divider" style="margin: 0.5rem 0;"></div>
                <p style="color: #e0e0e0; line-height: 1.6;">{response}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Please upload a resume first!")

if submit2:
    if uploaded_file is not None:
        with st.spinner("💡 Generating suggestions..."):
            file_content = extract_text_from_pdf(uploaded_file)
            response = get_llm_response(txt_input, file_content, input_prompt2)
            st.markdown(f"""
            <div class="response-box">
                <h4 style="color: white; margin: 0 0 0.5rem 0;">📈 Skill Improvement Suggestions</h4>
                <div class="custom-divider" style="margin: 0.5rem 0;"></div>
                <p style="color: #e0e0e0; line-height: 1.6;">{response}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Please upload a resume first!")

if submit3:
    if uploaded_file is not None:
        with st.spinner("🔑 Finding missing keywords..."):
            file_content = extract_text_from_pdf(uploaded_file)
            response = get_llm_response(txt_input, file_content, input_prompt3)
            st.markdown(f"""
            <div class="response-box">
                <h4 style="color: white; margin: 0 0 0.5rem 0;">🔍 Missing Keywords Analysis</h4>
                <div class="custom-divider" style="margin: 0.5rem 0;"></div>
                <p style="color: #e0e0e0; line-height: 1.6;">{response}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Please upload a resume first!")

if submit4:
    if uploaded_file is not None:
        with st.spinner("📊 Calculating percentage match..."):
            file_content = extract_text_from_pdf(uploaded_file)
            response = get_llm_response(txt_input, file_content, input_prompt4)
            st.markdown(f"""
            <div class="response-box">
                <h4 style="color: white; margin: 0 0 0.5rem 0;">🎯 Match Percentage Result</h4>
                <div class="custom-divider" style="margin: 0.5rem 0;"></div>
                <p style="color: #e0e0e0; line-height: 1.6;">{response}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Please upload a resume first!")