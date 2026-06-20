import streamlit as st

st.title("📊 PlacementGPT Dashboard")

st.write(
    "Welcome to PlacementGPT-AI"
)

resume_data = st.session_state.get(
    "resume_analysis",
    {}
)

feedback = st.session_state.get(
    "feedback",
    {}
)

# -----------------------------
# Resume Metrics
# -----------------------------

resume_score = resume_data.get(
    "resume_score",
    0
)

ats_score = resume_data.get(
    "ats_score",
    0
)

overall_score = feedback.get(
    "overall_score",
    0
)

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Resume Score",
        resume_score
    )

with col2:

    st.metric(
        "ATS Score",
        ats_score
    )

with col3:

    st.metric(
        "Interview Score",
        overall_score
    )

# -----------------------------
# Skills Metrics
# -----------------------------

profile = resume_data.get(
    "profile",
    {}
)

skill_gap = resume_data.get(
    "skill_gap",
    {}
)

questions = resume_data.get(
    "questions",
    []
)

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Skills Found",
        profile.get(
            "total_skills",
            0
        )
    )

with col2:

    st.metric(
        "Missing Skills",
        len(
            skill_gap.get(
                "missing_skills",
                []
            )
        )
    )

with col3:

    st.metric(
        "Questions Generated",
        len(questions)
    )

# -----------------------------
# Readiness Status
# -----------------------------

st.subheader(
    "🎯 Interview Readiness"
)

if overall_score >= 80:

    st.success(
        "🟢 Interview Ready"
    )

elif overall_score >= 60:

    st.warning(
        "🟡 Needs Minor Improvement"
    )

else:

    st.error(
        "🔴 Needs Significant Improvement"
    )

# -----------------------------
# Missing Skills
# -----------------------------

st.subheader(
    "⚠ Missing Skills"
)

for skill in skill_gap.get(
    "missing_skills",
    []
):

    st.warning(skill)

# -----------------------------
# Top Improvements
# -----------------------------

improvements = resume_data.get(
    "resume_improvements",
    {}
)

st.subheader(
    "🚀 Resume Improvements"
)

for item in improvements.get(
    "ats_recommendations",
    []
)[:5]:

    st.info(item)

# -----------------------------
# Strengths
# -----------------------------

if feedback:

    st.subheader(
        "💪 Strengths"
    )

    for item in feedback.get(
        "strengths",
        []
    ):

        st.success(item)