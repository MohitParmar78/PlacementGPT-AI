# Regular expressions
import re


def clean_resume_text(text: str) -> str:
    """
    Clean PDF text while preserving newlines.
    """

    # Remove extra spaces and tabs
    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    # Remove excessive blank lines
    text = re.sub(
        r"\n\s*\n+",
        "\n\n",
        text
    )

    return text.strip()


def extract_sections(text: str):
    """
    Extract resume sections.
    """

    sections = {
        "education": "",
        "skills": "",
        "projects": "",
        "experience": "",
        "certifications": "",
        "other": ""
    }

    # Split by lines
    lines = text.split("\n")

    current_section = "other"

    section_mapping = {

        "education":
            "education",

        "academic background":
            "education",

        "skills":
            "skills",

        "technical skills":
            "skills",

        "projects":
            "projects",

        "experience":
            "experience",

        "work experience":
            "experience",

        "certifications":
            "certifications"
    }

    for line in lines:

        line = line.strip()

        if not line:
            continue

        lower_line = line.lower()

        if lower_line in section_mapping:

            current_section = (
                section_mapping[lower_line]
            )

            continue

        sections[current_section] += (
            line + "\n"
        )

    return sections


def create_candidate_profile(
    file_name,
    sections,
    skills
):
    """
    Create candidate profile.
    """

    profile = {

        "resume_name":
            file_name,

        "skills":
            skills,

        "total_skills":
            len(skills),

        "education_found":
            bool(
                sections["education"]
            ),

        "experience_found":
            bool(
                sections["experience"]
            ),

        "certifications_found":
            bool(
                sections["certifications"]
            )
    }

    return profile

def generate_resume_stats(
    sections,
    skills
):
    """
    Generate resume statistics.
    """
    
    stats = {
        
        "skills_count":
            len(skills),

        "education_found":
            bool(
                sections["education"]
            ),

        "experience_found":
            bool(
                sections["experience"]
            ),

        "certifications_found":
            bool(
                sections["certifications"]
            )
    }

    return stats