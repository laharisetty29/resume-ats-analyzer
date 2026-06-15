import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from styles import GLOBAL_CSS
from components import hero_html
from layout import render_results
from extractor import extract_resume_text
from analyzer import analyze_resume

st.set_page_config(
    page_title="Resume ATS Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
st.markdown(hero_html(), unsafe_allow_html=True)

col_l, col_r = st.columns([1, 1], gap="large")

with col_l:
    st.markdown('<div class="sec-hd">📎 Upload Resume</div>', unsafe_allow_html=True)
    resume_file = st.file_uploader(
        "Supports PDF, DOCX, TXT",
        type=["pdf", "docx", "txt"],
        label_visibility="collapsed",
    )
    if resume_file:
        st.success(f"✅ Loaded: **{resume_file.name}**")

with col_r:
    st.markdown('<div class="sec-hd">📋 Job Description</div>', unsafe_allow_html=True)
    jd_text = st.text_area(
        "Paste the full job description here",
        height=180,
        placeholder="Paste job description here...",
        label_visibility="collapsed",
    )

st.markdown("<br>", unsafe_allow_html=True)
run_btn = st.button("🔍 Analyze Resume", use_container_width=True)

if run_btn:
    if not resume_file:
        st.error("⚠️ Please upload a resume file.")
    elif not jd_text.strip():
        st.error("⚠️ Please paste a job description.")
    else:
        with st.spinner("Analyzing with AI… this takes a few seconds."):
            try:
                resume_text = extract_resume_text(resume_file)
                result = analyze_resume(resume_text, jd_text)
                render_results(result)
            except ValueError as e:
                st.error(f"❌ AI response error: {e}")
            except Exception as e:
                st.error(f"❌ Unexpected error: {e}")