# ==========================================
# PlacementGPT-AI
# Embedding Model (Singleton)
# ==========================================

import os

# Heavy ML deps (torch + sentence-transformers) are optional at runtime.
# On memory-constrained deploys (e.g. Render free tier) they are left out of
# requirements entirely, so we import lazily and guard against absence
# instead of crashing the whole app at import time.
try:
    from sentence_transformers import SentenceTransformer
    _SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    _SENTENCE_TRANSFORMERS_AVAILABLE = False

# Set ENABLE_SEMANTIC_MATCH=false to skip loading the embedding model
# altogether (e.g. on low-memory deploys). Defaults to on for local/dev use.
SEMANTIC_MATCH_ENABLED = (
    os.getenv("ENABLE_SEMANTIC_MATCH", "true").lower() == "true"
    and _SENTENCE_TRANSFORMERS_AVAILABLE
)


class EmbeddingModel:

    _instance = None
    _model = None

    def __new__(cls):

        if cls._instance is None:

            cls._instance = super().__new__(cls)

        return cls._instance

    def get_model(self):

        if not SEMANTIC_MATCH_ENABLED:
            raise RuntimeError(
                "Semantic matching is disabled or sentence-transformers "
                "is not installed in this environment."
            )

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