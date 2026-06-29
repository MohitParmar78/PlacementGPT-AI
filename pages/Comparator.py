import streamlit as st
import requests
import os
import pandas as pd

st.set_page_config(page_title="Resume Comparator", page_icon="⚖️", layout="wide")

API_BASE_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.title("⚖️ Resume Comparator")
st.write("Compare two versions of a resume (e.g. before & after optimization) side-by-side to see the ATS impact.")

target_role = st.selectbox(
    "Select Target Role for Comparison",
    [
        "Software Engineer",
        "Backend Developer",
        "Frontend Developer",
        "Full Stack Developer",
        "Data Analyst",
        "Data Scientist",
        "Machine Learning Engineer",
        "Deep Learning Engineer",
        "GenAI Engineer",
        "AI Research Engineer",
        "DevOps Engineer",
        "Cloud Engineer"
    ]
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Resume Version A (e.g. Old)")
    resume_a = st.file_uploader("Upload Resume A (PDF)", type=["pdf"], key="res_a")

with col2:
    st.subheader("Resume Version B (e.g. New)")
    resume_b = st.file_uploader("Upload Resume B (PDF)", type=["pdf"], key="res_b")

if st.button("Compare Resumes", use_container_width=True):
    if resume_a is None or resume_b is None:
        st.warning("Please upload both resumes to compare.")
    else:
        with st.spinner("Analyzing both resumes... This may take a minute."):
            try:
                # Analyze A
                files_a = {"resume": (resume_a.name, resume_a, "application/pdf")}
                data_a = {"target_role": target_role, "difficulty": "Medium"}
                resp_a = requests.post(f"{API_BASE_URL}/analyze-resume", files=files_a, data=data_a, timeout=300)
                
                # Analyze B
                files_b = {"resume": (resume_b.name, resume_b, "application/pdf")}
                data_b = {"target_role": target_role, "difficulty": "Medium"}
                resp_b = requests.post(f"{API_BASE_URL}/analyze-resume", files=files_b, data=data_b, timeout=300)
                
                if resp_a.status_code == 200 and resp_b.status_code == 200:
                    res_a = resp_a.json()
                    res_b = resp_b.json()
                    
                    st.success("Comparison Complete!")
                    st.divider()
                    
                    # --- METRICS COMPARISON ---
                    st.subheader("📊 High-Level Metrics")
                    m1, m2, m3, m4 = st.columns(4)
                    
                    m1.metric("Resume A Score", f"{res_a.get('resume_score', 0)}/100")
                    m2.metric("Resume B Score", f"{res_b.get('resume_score', 0)}/100", 
                              delta=res_b.get('resume_score', 0) - res_a.get('resume_score', 0))
                              
                    m3.metric("ATS Score (A)", f"{res_a.get('ats_score', 0)}/100")
                    m4.metric("ATS Score (B)", f"{res_b.get('ats_score', 0)}/100", 
                              delta=res_b.get('ats_score', 0) - res_a.get('ats_score', 0))
                    
                    # --- SIDE BY SIDE DETAILS ---
                    st.divider()
                    st.subheader("🔍 Deep Dive Comparison")
                    
                    c1, c2 = st.columns(2)
                    
                    with c1:
                        st.write("### Resume A")
                        st.write(f"**Total Skills Found:** {res_a.get('profile', {}).get('total_skills', 0)}")
                        st.write("**Detected Skills:**")
                        st.info(", ".join(res_a.get('profile', {}).get('skills', [])))
                        st.write(f"**Missing Critical Skills ({len(res_a.get('skill_gap', {}).get('missing_skills', []))}):**")
                        for s in res_a.get('skill_gap', {}).get('missing_skills', []):
                            st.error(s)
                            
                    with c2:
                        st.write("### Resume B")
                        st.write(f"**Total Skills Found:** {res_b.get('profile', {}).get('total_skills', 0)}")
                        st.write("**Detected Skills:**")
                        st.info(", ".join(res_b.get('profile', {}).get('skills', [])))
                        st.write(f"**Missing Critical Skills ({len(res_b.get('skill_gap', {}).get('missing_skills', []))}):**")
                        for s in res_b.get('skill_gap', {}).get('missing_skills', []):
                            st.error(s)
                            
                else:
                    st.error(f"Error analyzing resumes. A: {resp_a.status_code}, B: {resp_b.status_code}")
            except Exception as e:
                st.error(f"An error occurred: {e}")
