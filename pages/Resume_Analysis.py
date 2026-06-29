# Streamlit
import streamlit as st

# Requests
import requests
import os
import streamlit.components.v1 as components

# API Config
API_BASE_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

def render_mermaid(code: str):
    components.html(
        f"""
        <div class="mermaid" style="display: flex; justify-content: center; background-color: white; padding: 20px; border-radius: 10px;">
            {code}
        </div>
        <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
            mermaid.initialize({{ startOnLoad: true, theme: 'default' }});
        </script>
        """,
        height=600, scrolling=True
    )


# Title
st.title("📄 Resume Analysis")

st.write(
    "Upload Resume for Parsing"
)

# File uploader
uploaded_file = st.file_uploader(
    "Choose Resume PDF",
    type=["pdf"]
)

# Target role selection
target_role = st.selectbox(
    "Select Target Role",
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

difficulty = st.selectbox(

    "Interview Difficulty",

    [
        "Easy",
        "Medium",
        "Hard"
    ]
)

# Analyze button
if st.button("Analyze Resume"):

    if uploaded_file is not None:

        api_url = f"{API_BASE_URL}/analyze-resume"

        files = {
            "resume": (
                uploaded_file.name,
                uploaded_file,
                "application/pdf"
            )
        }

        # Form data
        form_data = {

            "target_role":
            target_role,
            
            "difficulty":
            difficulty
        }

        # Send request
        with st.spinner(
            "Analyzing resume... This may take up to a minute on first startup."
        ):

            response = requests.post(
                api_url,
                files=files,
                data=form_data,
                timeout=300
            )

        if response.status_code == 200:

            data = response.json()
            
            st.session_state[
                "resume_analysis"
            ] = data
            
            st.session_state["target_role"] = data["target_role"]

            st.success(
                "Resume Analyzed Successfully"
            )
            
            st.subheader(
                "🧠 Multi-Agent Workflow Execution"
            )
            st.info("Visualizing the LangGraph AI Agents Orchestration Process:")
            
            try:
                from backend.workflows.interview_workflow import graph
                mermaid_code = graph.get_graph().draw_mermaid()
                render_mermaid(mermaid_code)
            except Exception as e:
                st.warning(f"Could not render workflow diagram: {e}")

            st.subheader(
                "📊 Resume Evaluation Dashboard"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Resume Score",
                    f"{data['resume_score']}/100"
                )

                st.progress(
                data["resume_score"] / 100
                )

            with col2:

                ats_score = data.get(
                    "ats_score",
                    0
                )

                st.metric(
                    "ATS Score",
                    f"{ats_score}/100"
                )

                st.progress(
                    ats_score / 100
                )
            
            st.subheader(
                "Score Breakdown"
            )

            breakdown = (
                data["score_breakdown"]
            )

            for key, value in breakdown.items():

                st.write(
                    f"{key.title()} : {value}"
                )
            
            # -----------------------------
            # Candidate Profile
            # -----------------------------

            profile = data["profile"]

            st.subheader(
                "👤 Candidate Profile"
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Skills",
                    profile.get(
                        "total_skills",
                        0
                    )
                )

            with col2:

                st.metric(
                    "Education",
                    "Yes"
                    if profile.get(
                        "education_found",
                        False
                    )
                    else "No"
                )

            with col3:

                st.metric(
                    "Experience",
                    "Yes"
                    if profile.get(
                    "experience_found",
                    False
                    )
                    else "No"
                )

            st.info(
                f"Target Role: {data['target_role']}"
            )
            
            # -----------------------------
            # Skill Gap Analysis
            # -----------------------------

            st.subheader(
                "🎯 Skill Gap Analysis"
            )
            
            st.subheader(
                "Detected Skills"
            )

            skills = (
                data["profile"]["skills"]
            )

            if skills:

                for skill in skills:

                    st.success(skill)

            else:

                st.warning(
                    "No skills detected"
                )

            skill_gap = data["skill_gap"]

            st.write(
                "### Missing Skills"
            )

            # Check if skills are missing
            if skill_gap["missing_skills"]:

                for skill in skill_gap["missing_skills"]:

                    st.warning(skill)

            else:

                st.success(
                    "No missing skills found!"
                )
            
            with st.expander(
                "View Required Skills"
            ):

                for skill in skill_gap[ "required_skills"]:

                    st.write(
                        f"✅ {skill}"
                    )
            
            # -----------------------------
            # ATS Analysis
            # -----------------------------

            ats_analysis = data.get(
                "ats_analysis",
                {}
            )

            st.subheader(
                "📌 ATS Analysis"
            )

            st.write(
                "### Matched Skills"
            )

            for skill in ats_analysis.get(
                "matched_skills",
                []
            ):

                st.success(skill)

            st.write(
                "### Matched Keywords"
            )

            for skill in ats_analysis.get(
                "missing_skills",
                []
            ):

                st.warning(skill)

            st.write(
                "### ATS Recommendations"
            )

            for recommendation in ats_analysis.get(
                "recommendations",
                []
            ):

                st.info(
                    recommendation
            )
                
            # -----------------------------
            # Resume Improvement Suggestions
            # -----------------------------

            improvements = data.get(
                "resume_improvements",
                {}
            )

            st.subheader(
                "🚀 Resume Improvement Suggestions"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.write(
                    "### Summary Improvements"
                )

                for item in improvements.get(
                    "summary_improvements",
                    []
                ):

                    st.info(item)

                st.write(
                    "### Project Improvements"
                )

                for item in improvements.get(
                    "project_improvements",
                    []
                ):

                    st.warning(item)

            with col2:

                st.write(
                    "### Experience Improvements"
                )

                for item in improvements.get(
                    "experience_improvements",
                    []
                ):

                    st.warning(item)

                st.write(
                    "### Skill Improvements"
                )

                for item in improvements.get(
                    "skill_improvements",
                    []
                ):

                    st.success(item)

            st.write(
                "### ATS Recommendations"
            )

            for item in improvements.get(
                "ats_recommendations",
                []
            ):

                st.error(item)
            
            # -----------------------------
            # Generated Questions
            # -----------------------------

            questions = data["questions"]
            
            st.session_state[
                "questions"
            ] = questions
            
            st.subheader(
                "Resume Statistics"
            )

            stats = data["stats"]

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Skills",
                        stats["skills_count"]
                )

                st.metric(
                    "Education",
                    "Yes" if stats["education_found"] else "No"
                )

            with col2:

                st.metric(
                    "Experience",
                    "Yes" if stats["experience_found"] else "No"
                )

                st.metric(
                    "Certifications",
                    "Yes" if stats["certifications_found"] else "No"
                )
            
            st.subheader(
                "Extracted Sections"
            )

            sections = data["sections"]

            for section_name, content in sections.items():

                with st.expander(
                    section_name.title()
                ):

                    st.write(content)      

            st.subheader(
                "Extracted Resume Text"
            )

            st.text_area(
                "Resume Content",
                data["resume_text"],
                height=350
            )