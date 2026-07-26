# ==========================================
# PlacementGPT-AI
# Semantic Matcher (Optimized)
# ==========================================

import difflib

# scikit-learn currently isn't a direct requirements.txt entry - it rides
# along as a transitive dependency of sentence-transformers. Guard it so
# the lean (no-ML) deploy build doesn't break on import.
try:
    from sklearn.metrics.pairwise import (
        cosine_similarity
    )
except ImportError:
    cosine_similarity = None

from backend.models.embedding_model import (
    EmbeddingModel,
    SEMANTIC_MATCH_ENABLED
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
        # Fall back to a lightweight, dependency-free
        # string similarity check if the ML embedding
        # model is disabled or unavailable (e.g. on a
        # memory-constrained deploy). Keeps the API
        # response shape identical either way.
        # ------------------------------------

        if not SEMANTIC_MATCH_ENABLED:

            return self._match_skills_fallback(
                resume_skills,
                target_skills,
                threshold
            )

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

    def _match_skills_fallback(
        self,
        resume_skills,
        target_skills,
        threshold=0.75
    ):
        """
        Lightweight substitute for match_skills() that uses
        difflib string similarity instead of ML embeddings.
        No torch / sentence-transformers required, so it's
        safe to run on low-memory deploys.
        """

        matched = []
        missing = []

        for target_skill in target_skills:

            if self.exact_match(resume_skills, target_skill):

                matched.append(
                    {
                        "target_skill": target_skill,
                        "matched_skill": target_skill,
                        "similarity": 1.0
                    }
                )
                continue

            best_match = None
            best_score = 0.0

            for skill in resume_skills:

                score = difflib.SequenceMatcher(
                    None,
                    target_skill.lower().strip(),
                    skill.lower().strip()
                ).ratio()

                if score > best_score:
                    best_score = score
                    best_match = skill

            if best_match is not None and best_score >= threshold:

                matched.append(
                    {
                        "target_skill": target_skill,
                        "matched_skill": best_match,
                        "similarity": round(best_score, 3)
                    }
                )
            else:

                missing.append(
                    {
                        "target_skill": target_skill,
                        "best_match": best_match,
                        "similarity": round(best_score, 3)
                    }
                )

        return {
            "matched": matched,
            "missing": missing
        }