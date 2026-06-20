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
    
    # =====================================
    # EXECUTIVE SUMMARY
    # =====================================

    content.append(

        Paragraph(

            "Placement Readiness Summary",

            styles["Heading1"]
        )
    )

    content.append(

        Paragraph(

            f"Resume Score: {resume_score}/100",

            styles["BodyText"]
        )
    )

    content.append(

        Paragraph(

            f"ATS Score: {ats_score}/100",

            styles["BodyText"]
        )
    )

    content.append(

        Paragraph(

            f"Interview Score: {overall_score}/100",

            styles["BodyText"]
        )
    )

    content.append(

        Paragraph(

            f"Readiness Level: {readiness}",

            styles["Heading2"]
        )
    )

    content.append(
        Spacer(1, 20)
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

           f"Education Section: "
           f"{'Present' if profile.get('education_found') else 'Missing'}",

            styles["BodyText"]
        )
    )

    content.append(

        Paragraph(

            f"Experience Section: "
            f"{'Present' if profile.get('experience_found') else 'Missing'}",

            styles["BodyText"]
        )
    )
    
    content.append(

        Paragraph(

            f"Certifications Section: "
            f"{'Present' if profile.get('certifications_found') else 'Missing'}",

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

                f"✓ {skill}",

                styles["BodyText"]
            )
        )

    for skill in ats_analysis.get(
        "missing_skills",
        []
    ):

        content.append(

            Paragraph(

                f"✗ {skill}",

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
    
    sections_map = {

    "summary_improvements":
        "Summary Improvements",

    "project_improvements":
        "Project Improvements",

    "experience_improvements":
        "Experience Improvements",

    "skill_improvements":
        "Skill Improvements",

    "ats_recommendations":
        "ATS Recommendations"
    }

    for key, heading in sections_map.items():

        items = resume_improvements.get(
            key,
            []
        )

        if not items:
            continue

        content.append(

            Paragraph(

                heading,

                styles["Heading2"]
            )
        )

        for item in items:

            content.append(

                Paragraph(

                    f"• {item}",

                    styles["BodyText"]
                )
            )

        content.append(
            Spacer(1, 10)
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
    
    content.append(
        PageBreak()
    )

    content.append(

        Paragraph(

            "Final Assessment",

            styles["Title"]
        )
    )

    content.append(
        Spacer(1, 20)
    )

    content.append(

        Paragraph(

            f"Resume Score: {resume_score}/100",

            styles["BodyText"]
        )
    )

    content.append(

        Paragraph(

            f"ATS Score: {ats_score}/100",

            styles["BodyText"]
        )
    )

    content.append(

        Paragraph(

            f"Interview Score: {overall_score}/100",

            styles["BodyText"]
        )
    )

    content.append(

        Paragraph(

            f"Readiness Level: {readiness}",

            styles["Heading2"]
        )
    )

    content.append(
        Spacer(1, 20)
    )

    if overall_score >= 80:

        recommendation = (
            "Candidate is interview-ready and demonstrates strong technical understanding."
        )

    elif overall_score >= 60:

        recommendation = (
            "Candidate has a solid foundation but should improve technical depth and communication."
        )

    else:

        recommendation = (
            "Candidate should strengthen fundamentals and practice more interview questions."
        )

    content.append(

        Paragraph(

            "Final Recommendation",

            styles["Heading1"]
        )
    )

    content.append(

        Paragraph(

            recommendation,

            styles["BodyText"]
        )
    )

    doc.build(
        content
    )

    return output_path