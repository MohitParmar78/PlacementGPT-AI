# ==========================================
# PlacementGPT-AI
# Embedding Model
# ==========================================

from sentence_transformers import (
    SentenceTransformer
)


class EmbeddingModel:

    def __init__(self):

        self.model = None

    def get_model(self):

        if self.model is None:

            print(
                "Loading embedding model..."
            )

            self.model = SentenceTransformer(
                "all-MiniLM-L6-v2"
            )

        return self.model

    def encode_text(
        self,
        text
    ):

        model = self.get_model()

        embedding = model.encode(

            text,

            normalize_embeddings=True
        )

        return embedding

    def encode_batch(
        self,
        texts
    ):

        model = self.get_model()

        embeddings = model.encode(

            texts,

            normalize_embeddings=True
        )

        return embeddings