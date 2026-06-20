# ==========================================
# PlacementGPT-AI
# PDF Report Agent
# ==========================================

import os

from reportlab.platypus import (

    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)


def generate_pdf_report(

    target_role,

    profile,

    resume_score,

    ats_score,

    skill_gap,

    ats_analysis,

    resume_improvements,

    interview_feedback,

    output_path=
    "reports/PlacementGPT_Report.pdf"
):
    """
    Generate PlacementGPT PDF Report
    """

    os.makedirs(
        "reports",
        exist_ok=True
    )

    doc = SimpleDocTemplate(
        output_path
    )

    styles = (
        getSampleStyleSheet()
    )

    content = []

    # =====================================
    # TITLE PAGE
    # =====================================

    content.append(

        Paragraph(

            "PlacementGPT-AI Assessment Report",

            styles["Title"]
        )
    )

    content.append(
        Spacer(1, 20)
    )

    content.append(

        Paragraph(

            f"Target Role: {target_role}",

            styles["Heading2"]
        )
    )

    content.append(
        Spacer(1, 20)
    )

    overall_score = interview_feedback.get(
        "overall_score",
        0
    )

    if overall_score >= 80:

        readiness = (
            "Interview Ready"
        )

    elif overall_score >= 60:

        readiness = (
            "Needs Minor Improvement"
        )

    else:

        readiness = (
            "Needs Significant Improvement"
        )

    content.append(

        Paragraph(

            f"Interview Readiness: "
            f"{readiness}",

            styles["Heading2"]
        )
    )

    content.append(
        Spacer(1, 30)
    )
    
    # =====================================
    # RESUME ANALYSIS
    # =====================================

    content.append(

        Paragraph(

            "Resume Analysis",

            styles["Heading1"]
        )
    )

    content.append(

        Paragraph(

            f"Resume Score: "
            f"{resume_score}/100",

            styles["BodyText"]
        )
    )

    content.append(

        Paragraph(

            f"ATS Score: "
            f"{ats_score}/100",

            styles["BodyText"]
        )
    )

    content.append(
        Spacer(1, 20)
    )
    
    # =====================================
    # CANDIDATE PROFILE
    # =====================================

    content.append(

        Paragraph(

            "Candidate Profile",

            styles["Heading1"]
        )   
    )

    content.append(

        Paragraph(

            f"Total Skills: "
            f"{profile.get('total_skills',0)}",

            styles["BodyText"]
        )
    )

    content.append(

        Paragraph(

            f"Education Found: "
            f"{profile.get('education_found',False)}",

            styles["BodyText"]
        )
    )

    content.append(

        Paragraph(

            f"Experience Found: "
            f"{profile.get('experience_found',False)}",

            styles["BodyText"]
        )
    )

    content.append(
        Spacer(1, 20)
    )
    
    # =====================================
    # SKILL GAP ANALYSIS    
    # =====================================

    content.append(

        Paragraph(

            "Skill Gap Analysis",

            styles["Heading1"]
        )
    )

    content.append(

        Paragraph(

            "Missing Skills",

            styles["Heading2"]
        )
    )

    for skill in skill_gap.get(
        "missing_skills",
        []
    ):

        content.append(

            Paragraph(

                f"• {skill}",

                styles["BodyText"]
            )
        )
    
    content.append(
        Spacer(1, 20)
    )
    
    # =====================================
    # ATS ANALYSIS
    # =====================================

    content.append(

        Paragraph(

            "ATS Analysis",

            styles["Heading1"]
        )
    )

    for skill in ats_analysis.get(
        "matched_skills",
        []
    ):

        content.append(

            Paragraph(

                f"Matched: {skill}",

                styles["BodyText"]
            )
        )

    for skill in ats_analysis.get(
        "missing_skills",
        []
    ):

        content.append(

            Paragraph(

                f"Missing: {skill}",

                styles["BodyText"]
            )
        )
    
    content.append(
        Spacer(1, 20)
    )
    
    # =====================================
    # RESUME IMPROVEMENTS
    # =====================================

    content.append(

        Paragraph(

            "Resume Improvement Suggestions",

            styles["Heading1"]
        )
    )

    for section in [

        "summary_improvements",

        "project_improvements",

        "experience_improvements",

        "skill_improvements",

        "ats_recommendations"
    ]:

        for item in resume_improvements.get(
            section,
            []
        ):

            content.append(

                Paragraph(

                    f"• {item}",

                    styles["BodyText"]
                )
            )
        
        content.append(
        Spacer(1, 20)
    )

    # =====================================
    # SCORES
    # =====================================

    content.append(

        Paragraph(

            "Interview Scores",

            styles["Heading1"]
        )
    )

    content.append(

        Paragraph(

            f"Overall Score: "
            f"{overall_score}/100",

            styles["BodyText"]
        )
    )

    content.append(

        Paragraph(

            f"Technical Score: "
            f"{interview_feedback.get('technical_score',0)}/10",

            styles["BodyText"]
        )
    )

    content.append(

        Paragraph(

            f"Communication Score: "
            f"{interview_feedback.get('communication_score',0)}/10",

            styles["BodyText"]
        )
    )

    content.append(
        PageBreak()
    )
    
    content.append(
        Spacer(1, 20)
    )

    # =====================================
    # QUESTION FEEDBACK
    # =====================================

    content.append(

        Paragraph(

            "Question Wise Evaluation",

            styles["Heading1"]
        )
    )

    for index, item in enumerate(

        interview_feedback.get(
            "question_feedback",
            []
        ),

        start=1
    ):

        content.append(

            Paragraph(

                f"Question {index}",

                styles["Heading2"]
            )
        )

        content.append(

            Paragraph(

                item.get(
                    "question",
                    ""
                ),

                styles["BodyText"]
            )
        )

        content.append(

            Paragraph(

                f"Score: "
                f"{item.get('score',0)}/10",

                styles["BodyText"]
            )
        )

        content.append(

            Paragraph(

                f"Feedback: "
                f"{item.get('feedback','')}",

                styles["BodyText"]
            )
        )

        content.append(

            Paragraph(

                f"Ideal Answer:",

                styles["Heading3"]
            )
        )

        content.append(

            Paragraph(

                item.get(
                    "correct_answer",
                    ""
                ),

                styles["BodyText"]
            )
        )

        content.append(
            Spacer(1, 20)
        )

    content.append(
        PageBreak()
    )
    
    content.append(
        Spacer(1, 20)
    )

    # =====================================
    # STRENGTHS
    # =====================================

    content.append(

        Paragraph(

            "Strengths",

            styles["Heading1"]
        )
    )

    for strength in interview_feedback.get(
        "strengths",
        []
    ):

        content.append(

            Paragraph(

                f"• {strength}",

                styles["BodyText"]
            )
        )

    content.append(
        Spacer(1, 20)
    )

    # =====================================
    # WEAKNESSES
    # =====================================

    content.append(

        Paragraph(

            "Weaknesses",

            styles["Heading1"]
        )
    )

    for weakness in interview_feedback.get(
        "weaknesses",
        []
    ):

        content.append(

            Paragraph(

                f"• {weakness}",

                styles["BodyText"]
            )
        )

    content.append(
        Spacer(1, 20)
    )

    # =====================================
    # IMPROVEMENTS
    # =====================================

    content.append(

        Paragraph(

            "Improvement Suggestions",

            styles["Heading1"]
        )
    )

    for suggestion in interview_feedback.get(
        "improvement_suggestions",
        []
    ):

        content.append(

            Paragraph(

                f"• {suggestion}",

                styles["BodyText"]
            )
        )

    content.append(
        PageBreak()
    )

    # =====================================
    # LEARNING ROADMAP
    # =====================================

    content.append(

        Paragraph(

            "Learning Roadmap",

            styles["Heading1"]
        )
    )

    for item in interview_feedback.get(
        "learning_roadmap",
        []
    ):

        content.append(

            Paragraph(

                f"• {item}",

                styles["BodyText"]
            )
        )

    doc.build(
        content
    )

    return output_path