# ==========================================
# PlacementGPT-AI
# Embedding Model (Singleton)
# ==========================================

from sentence_transformers import SentenceTransformer


class EmbeddingModel:

    _instance = None
    _model = None

    def __new__(cls):

        if cls._instance is None:

            cls._instance = super().__new__(cls)

        return cls._instance

    def get_model(self):

        if EmbeddingModel._model is None:

            print("Loading embedding model...")

            EmbeddingModel._model = SentenceTransformer(
                "all-MiniLM-L6-v2"
            )

        return EmbeddingModel._model

    def encode_text(
        self,
        text
    ):

        model = self.get_model()

        return model.encode(

            text,

            normalize_embeddings=True
        )

    def encode_batch(
        self,
        texts
    ):

        model = self.get_model()

        return model.encode(

            texts,

            normalize_embeddings=True
        )