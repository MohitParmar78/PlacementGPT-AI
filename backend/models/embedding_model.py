# ==========================================
# PlacementGPT-AI
# Embedding Model
# ==========================================

from sentence_transformers import (
    SentenceTransformer
)


class EmbeddingModel:
    """
    Generate semantic embeddings
    for resumes, skills, and job roles.
    """

    def __init__(self):

        self.model = SentenceTransformer(
            "BAAI/bge-small-en-v1.5"
        )

    def encode_text(
        self,
        text
    ):
        """
        Convert text into embedding.

        Parameters
        ----------
        text : str

        Returns
        -------
        list
        """

        embedding = self.model.encode(
            text,
            normalize_embeddings=True
        )

        return embedding

    def encode_batch(
        self,
        texts
    ):
        """
        Convert multiple texts
        into embeddings.
        """

        embeddings = self.model.encode(

            texts,

            normalize_embeddings=True
        )

        return embeddings