import streamlit as st
import requests
import os
import json

st.set_page_config(page_title="Interview History", page_icon="📜", layout="wide")

API_BASE_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.title("📜 Interview History & Progress")
st.write("Track your past performance and continuous improvements.")

try:
    response = requests.get(f"{API_BASE_URL}/history?limit=10", timeout=10)
    
    if response.status_code == 200:
        history = response.json()
        
        if not history:
            st.info("No interview history found. Complete an interview to see your progress here!")
        else:
            for session in history:
                with st.expander(f"{session['created_at'][:10]} - {session['target_role']} (Score: {session['overall_score']}/100) - {session['readiness']}"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Technical Score", session['technical_score'])
                    with col2:
                        st.metric("Communication Score", session['communication_score'])
                    with col3:
                        st.metric("Overall Score", session['overall_score'])
                    
                    st.divider()
                    
                    colA, colB = st.columns(2)
                    with colA:
                        st.subheader("✅ Strengths")
                        for s in session.get('strengths', []):
                            st.success(s)
                            
                        st.subheader("🚀 Improvement Suggestions")
                        for s in session.get('improvement_suggestions', []):
                            st.info(s)
                            
                    with colB:
                        st.subheader("⚠️ Weaknesses")
                        for w in session.get('weaknesses', []):
                            st.warning(w)
                            
                        st.subheader("📚 Learning Roadmap")
                        for r in session.get('learning_roadmap', []):
                            st.write(f"- {r}")
                            
                    st.subheader("📝 Question Feedback")
                    for qf in session.get('question_feedback', []):
                        st.write(f"**Q:** {qf.get('question', '')}")
                        st.write(f"**Score:** {qf.get('score', 0)}/10")
                        st.warning(f"**Feedback:** {qf.get('feedback', '')}")
                        st.success(f"**Expected:** {qf.get('correct_answer', '')}")
                        st.markdown("---")
    else:
        st.error(f"Failed to fetch history: HTTP {response.status_code}")
except Exception as e:
    st.error(f"Could not connect to backend: {e}")
