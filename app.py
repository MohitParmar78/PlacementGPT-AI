import streamlit as st

st.set_page_config(
    page_title="PlacementGPT-AI",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 PlacementGPT-AI")

st.markdown(
    """
### AI-Powered Career Preparation Platform

Prepare smarter for placements using AI-driven resume analysis,
ATS optimization, interview simulations, and personalized learning roadmaps.
"""
)

st.divider()

col1, col2 = st.columns(2)

with col1:

    st.subheader("📄 Resume Intelligence")

    st.write("• Resume Parsing")
    st.write("• ATS Scoring")
    st.write("• Skill Gap Analysis")
    st.write("• Resume Improvements")

with col2:

    st.subheader("🎤 Interview Preparation")

    st.write("• AI Interview Questions")
    st.write("• Follow-Up Questions")
    st.write("• Answer Evaluation")
    st.write("• Career Roadmaps")

st.divider()

st.subheader("🛠 Tech Stack")

tech1, tech2, tech3 = st.columns(3)

with tech1:
    st.success("FastAPI")
    st.success("Streamlit")

with tech2:
    st.success("LangGraph")
    st.success("Groq LLM")

with tech3:
    st.success("Sentence Transformers")
    st.success("Scikit-Learn")

st.divider()

st.info(
    "Upload a resume from the Resume Analysis page to begin."
)