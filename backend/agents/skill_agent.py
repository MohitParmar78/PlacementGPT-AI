import pandas as pd
import re


def load_skill_database():

    skills_df = pd.read_csv(
        "data/skills/skills.csv"
    )

    return skills_df["skill"].tolist()


def extract_skills(
    skills_section
):
    """
    Extract skills using regex.
    """

    skills_database = (
        load_skill_database()
    )

    detected_skills = []

    for skill in skills_database:

        pattern = (
            r"\b"
            + re.escape(skill)
            + r"\b"
        )

        if re.search(
            pattern,
            skills_section,
            re.IGNORECASE
        ):

            detected_skills.append(
                skill
            )

    return sorted(
        list(set(detected_skills))
    )