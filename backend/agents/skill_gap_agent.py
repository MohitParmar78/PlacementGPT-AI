# ==========================================
# PlacementGPT-AI
# Skill Gap Agent
# ==========================================

from backend.models.semantic_matcher import (
    SemanticMatcher
)


class SkillGapAgent:
    """
    Identify missing skills
    using semantic similarity.
    """

    def __init__(self):

        self.matcher = (
            SemanticMatcher()
        )

    def analyze_skill_gap(
        self,
        resume_skills,
        target_skills,
        target_role
    ):
        """
        Analyze skill gaps.
        """

        result = self.matcher.match_skills(

            resume_skills=
                resume_skills,

            target_skills=
                target_skills
        )

        matched_skills = []

        missing_skills = []

        for item in result[
            "matched"
        ]:

            matched_skills.append(

                {

                    "target_skill":
                        item[
                            "target_skill"
                        ],

                    "matched_skill":
                        item[
                            "matched_skill"
                        ],

                    "similarity":
                        item[
                            "similarity"
                        ]
                }
            )

        for item in result[
            "missing"
        ]:

            missing_skills.append(

                item[
                    "target_skill"
                ]
            )

        return {

            "target_role":
                target_role,

            "required_skills":
                target_skills,

            "matched_skills":
                matched_skills,

            "missing_skills":
                missing_skills
        }