# ==========================================
# PlacementGPT-AI
# Interview Feedback Page
# ==========================================

import streamlit as st
import os

from backend.agents.report_agent import (
    generate_pdf_report
)

# ------------------------------------------
# Page Config
# ------------------------------------------

st.set_page_config(
    page_title="Interview Feedback",
    page_icon="📊",
    layout="wide"
)

# ------------------------------------------
# Page Title
# ------------------------------------------

st.title(
    "📊 Interview Feedback"
)

# ------------------------------------------
# Check Feedback Exists
# ------------------------------------------

if "feedback" not in st.session_state:

    st.warning(
        "Complete interview first."
    )

    st.stop()

# ------------------------------------------
# Load Feedback
# ------------------------------------------

feedback = st.session_state["feedback"]

resume_data = st.session_state.get(
    "resume_analysis",
    {}
)

# ------------------------------------------
# Scores
# ------------------------------------------

st.subheader(
    "Interview Scores"
)

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Overall Score",
        feedback.get(
            "overall_score",
            0
        )
    )

with col2:

    st.metric(
        "Technical Score",
        feedback.get(
            "technical_score",
            0
        )
    )
    
    overall_score = feedback.get(
        "overall_score",
        0
    )

    st.progress(
        overall_score / 100
    )

with col3:

    st.metric(
        "Communication Score",
        feedback.get(
            "communication_score",
            0
        )
    )
    
st.subheader(
    "🎯 Interview Readiness"
)

readiness = feedback.get(
    "readiness",
    "Unknown"
)

if readiness == "Interview Ready":

    st.success(readiness)

elif readiness == "Needs Minor Improvement":

    st.warning(readiness)

else:

    st.error(readiness)

# ------------------------------------------
# Strengths
# ------------------------------------------

st.subheader(
    "✅ Strengths"
)

strengths = feedback.get(
    "strengths",
    []
)

if strengths:

    for strength in strengths:

        st.success(
            strength
        )

else:

    st.info(
        "No strengths detected."
    )

# ------------------------------------------
# Weaknesses
# ------------------------------------------

st.subheader(
    "⚠ Weaknesses"
)

weaknesses = feedback.get(
    "weaknesses",
    []
)

if weaknesses:

    for weakness in weaknesses:

        st.warning(
            weakness
        )

else:

    st.info(
        "No weaknesses detected."
    )

# ------------------------------------------
# Improvement Suggestions
# ------------------------------------------

st.subheader(
    "🚀 Improvement Suggestions"
)

suggestions = feedback.get(
    "improvement_suggestions",
    []
)

if suggestions:

    for suggestion in suggestions:

        st.info(
            suggestion
        )

else:

    st.info(
        "No suggestions available."
    )

# ------------------------------------------
# Learning Roadmap
# ------------------------------------------

st.subheader(
    "📚 Learning Roadmap"
)

roadmap = feedback.get(
    "learning_roadmap",
    []
)

if roadmap:

    for step in roadmap:

        st.write(
            f"📌 {step}"
        )

else:

    st.info(
        "No roadmap generated."
    )

st.subheader(
    "📝 Question-wise Analysis"
)

question_feedback = feedback.get(
    "question_feedback",
    []
)

for item in question_feedback:

    with st.expander(
        item["question"]
    ):

        st.write(
            f"Score: {item['score']}/10"
        )

        st.warning(
            item["feedback"]
        )

        st.success(
            item["correct_answer"]
        )

st.markdown("---")

st.subheader(
    "📄 Generate Report"
)

if st.button(
    "Generate PDF Report"
):
    pdf_path = generate_pdf_report(

        target_role=
            st.session_state.get(
                "target_role",
                ""
            ),

        profile=
            resume_data.get(
                "profile",
                {}
            ),

        resume_score=
            resume_data.get(
                "resume_score",
                0
            ),

        ats_score=
            resume_data.get(
                "ats_score",
                0
            ),

        skill_gap=
            resume_data.get(
                "skill_gap",
                {}
            ),

        ats_analysis=
            resume_data.get(
                "ats_analysis",
                {}
            ),

        resume_improvements=
            resume_data.get(
                "resume_improvements",
                {}
            ),

        interview_feedback=
            feedback
    )

    st.success(
        "PDF Generated Successfully"
    )

    with open(
        pdf_path,
        "rb"
    ) as file:

        st.download_button(

            label=
                "⬇ Download Report",

            data=
                file,

            file_name=
                "PlacementGPT_Report.pdf",

            mime=
                "application/pdf"
        )