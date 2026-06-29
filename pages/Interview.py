# ==========================================
# PlacementGPT-AI
# Interview Page
# ==========================================

import requests
import streamlit as st
import os
import streamlit.components.v1 as components

API_BASE_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

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

def render_timer(minutes: int):
    components.html(
        f"""
        <div id="timer" style="font-family: sans-serif; font-size: 24px; font-weight: bold; color: #2e7d32; text-align: center; padding: 10px; border: 2px solid #2e7d32; border-radius: 10px; background-color: #e8f5e9;">
            Time Remaining: {minutes}:00
        </div>
        <script>
            let timeLeft = {minutes * 60};
            let timerEl = document.getElementById('timer');
            
            let countdown = setInterval(function() {{
                timeLeft -= 1;
                let m = Math.floor(timeLeft / 60);
                let s = timeLeft % 60;
                
                if(s < 10) s = '0' + s;
                
                timerEl.innerHTML = "Time Remaining: " + m + ":" + s;
                
                if (timeLeft <= 60 && timeLeft > 0) {{
                    timerEl.style.color = '#ef6c00';
                    timerEl.style.borderColor = '#ef6c00';
                    timerEl.style.backgroundColor = '#fff3e0';
                }}
                
                if (timeLeft <= 0) {{
                    clearInterval(countdown);
                    timerEl.innerHTML = "TIME IS UP! PLEASE WRAP UP YOUR ANSWER.";
                    timerEl.style.color = '#c62828';
                    timerEl.style.borderColor = '#c62828';
                    timerEl.style.backgroundColor = '#ffebee';
                    // Optional: play an alert sound
                    let audio = new Audio('https://actions.google.com/sounds/v1/alarms/beep_short.ogg');
                    audio.play().catch(e => console.log(e));
                }}
            }}, 1000);
        </script>
        """,
        height=80
    )

st.write("### ⏱️ Interview Timer")
render_timer(5) # Set 5 minutes for the overall interview or per question? We'll set 15 minutes overall for realism.


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

                f"{API_BASE_URL}/generate-followup",

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

st.markdown("---")
st.warning("⏱️ When you are finished or time is up, click below to evaluate your responses.")

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
                f"{API_BASE_URL}/evaluate-interview",
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