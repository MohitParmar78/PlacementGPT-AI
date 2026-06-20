# ==========================================
# PlacementGPT-AI
# Interview Page
# ==========================================

import requests
import streamlit as st

# ------------------------------------------
# Page Configuration
# ------------------------------------------

st.set_page_config(
    page_title="Interview Session",
    page_icon="🎤",
    layout="wide"
)

# ------------------------------------------
# Page Title
# ------------------------------------------

st.title("🎤 AI Interview Session")

st.write(
    """
    Answer the interview questions generated
    from your resume analysis.
    """
)

# ------------------------------------------
# Check Resume Analysis Completed
# ------------------------------------------

if "questions" not in st.session_state:

    st.warning(
        "Please analyze your resume first."
    )

    st.stop()

# ------------------------------------------
# Load Questions
# ------------------------------------------

questions = st.session_state["questions"]

# ------------------------------------------
# Display Questions
# ------------------------------------------

st.subheader(
    "Generated Interview Questions"
)

for index, question_data in enumerate(
    questions,
    start=1
):

    st.markdown("---")

    st.subheader(
        f"Question {index}"
    )

    st.write(
        f"**Skill:** {question_data['skill']}"
    )

    st.write(
        f"**Question:** {question_data['question']}"
    )

    st.text_area(
        label=f"Your Answer {index}",
        key=f"answer_{index}",
        height=150
    )
    
    if st.button(
        f"Generate Follow-Up {index}"
    ):

        answer = st.session_state.get(
            f"answer_{index}",
            ""
        )

        if answer.strip() == "":

            st.warning(
                "Please answer first."
            )

        else:

            response = requests.post(

                "http://127.0.0.1:8000/generate-followup",

                json={

                    "question":
                        question_data["question"],

                    "answer":
                        answer,

                    "skill":
                        question_data["skill"],

                    "target_role":
                        st.session_state.get(
                            "target_role",
                            ""
                        )
                }
            )

            if response.status_code == 200:

                followup = response.json()

                st.info(

                    followup.get(
                        "followup_question",
                        ""
                    )
                )

            else:

                st.error(
                    "Failed to generate follow-up."
                )

# ------------------------------------------
# Evaluate Interview
# ------------------------------------------

if st.button(
    "Evaluate Interview",
    use_container_width=True
):

    interview_data = []

    for index, question_data in enumerate(
        questions,
        start=1
    ):

        answer = st.session_state.get(
            f"answer_{index}",
            ""
        )

        interview_data.append(
            {
                "question": question_data["question"],
                "skill": question_data["skill"],
                "answer": answer
            }
        )

    # --------------------------------------
    # Get Target Role
    # --------------------------------------

    role = st.session_state.get(
        "target_role",
        "Machine Learning Engineer"
    )

    # --------------------------------------
    # API Call
    # --------------------------------------

    try:

        with st.spinner(
            "Evaluating Interview..."
        ):

            response = requests.post(
                "http://127.0.0.1:8000/evaluate-interview",
                json={
                    "target_role": role,
                    "interview": interview_data
                },
                timeout=300
            )

        # ----------------------------------
        # Backend Error
        # ----------------------------------

        if response.status_code != 200:

            st.error(
                f"Backend Error: {response.status_code}"
            )

            st.code(
                response.text
            )

            st.stop()

        # ----------------------------------
        # Parse Response
        # ----------------------------------

        feedback = response.json()

        overall_score = feedback.get(
            "overall_score",
            0
        )

        # ----------------------------------
        # Readiness Classification
        # ----------------------------------

        if overall_score >= 80:

            readiness = "Interview Ready"

        elif overall_score >= 60:

            readiness = (
                "Needs Minor Improvement"
            )

        else:

            readiness = (
                "Needs Significant Improvement"
            )

        feedback["readiness"] = readiness

        # ----------------------------------
        # Save Session State
        # ----------------------------------

        st.session_state[
            "feedback"
        ] = feedback

        st.session_state[
            "roadmap"
        ] = feedback.get(
            "learning_roadmap",
            []
        )

        st.session_state[
            "interview_score"
        ] = overall_score

        # ----------------------------------
        # Success Messages
        # ----------------------------------

        st.success(
            "Interview Evaluation Completed"
        )

        st.metric(
            "Overall Score",
            f"{overall_score}/100"
        )

        st.info(
            f"Readiness Status: {readiness}"
        )
        
        st.switch_page("pages/Feedback.py")

    except Exception as e:

        st.error(
            f"Error: {str(e)}"
        )