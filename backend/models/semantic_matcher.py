# ==========================================
# PlacementGPT-AI
# Semantic Matcher (Optimized)
# ==========================================

from sklearn.metrics.pairwise import (
    cosine_similarity
)

from backend.models.embedding_model import (
    EmbeddingModel
)


class SemanticMatcher:
    """
    Semantic similarity matcher
    using embeddings.
    """

    def __init__(self):

        self.embedding_model = (
            EmbeddingModel()
        )

    def exact_match(
        self,
        resume_skills,
        target_skill
    ):
        """
        Check exact skill match.
        """

        target_skill = (
            target_skill
            .lower()
            .strip()
        )

        for skill in resume_skills:

            if (
                skill.lower().strip()
                ==
                target_skill
            ):

                return True

        return False

    def match_skills(
        self,
        resume_skills,
        target_skills,
        threshold=0.75
    ):
        """
        Match resume skills
        with target skills.
        """

        matched = []

        missing = []

        # ------------------------------------
        # Handle Empty Lists
        # ------------------------------------

        if not resume_skills or not target_skills:

            return {

                "matched": matched,

                "missing": missing
            }

        # ------------------------------------
        # Encode Resume Skills Once
        # ------------------------------------

        resume_embeddings = (
            self.embedding_model
            .encode_batch(
                resume_skills
            )
        )

        # ------------------------------------
        # Encode Target Skills Once
        # ------------------------------------

        target_embeddings = (
            self.embedding_model
            .encode_batch(
                target_skills
            )
        )

        # ------------------------------------
        # Similarity Matrix
        #
        # Rows    -> Target Skills
        # Columns -> Resume Skills
        # ------------------------------------

        similarity_matrix = cosine_similarity(

            target_embeddings,

            resume_embeddings

        )

        # ------------------------------------
        # Process Each Target Skill
        # ------------------------------------

        for i, target_skill in enumerate(
            target_skills
        ):

            # -----------------------------
            # Exact Match
            # -----------------------------

            if self.exact_match(

                resume_skills,

                target_skill

            ):

                matched.append(

                    {

                        "target_skill":
                            target_skill,

                        "matched_skill":
                            target_skill,

                        "similarity":
                            1.0
                    }
                )

                continue

            # -----------------------------
            # Best Semantic Match
            # -----------------------------

            row = similarity_matrix[i]

            best_index = row.argmax()

            best_score = float(
                row[best_index]
            )

            best_match = (
                resume_skills[
                    best_index
                ]
            )

            if best_score >= threshold:

                matched.append(

                    {

                        "target_skill":
                            target_skill,

                        "matched_skill":
                            best_match,

                        "similarity":
                            round(
                                best_score,
                                3
                            )
                    }
                )

            else:

                missing.append(

                    {

                        "target_skill":
                            target_skill,

                        "best_match":
                            best_match,

                        "similarity":
                            round(
                                best_score,
                                3
                            )
                    }
                )

        return {

            "matched":
                matched,

            "missing":
                missing
        }