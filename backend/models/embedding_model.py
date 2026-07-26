# ==========================================
# PlacementGPT-AI
# Embedding Model (Singleton)
# ==========================================

import os
import time

import numpy as np
import requests

# Heavy ML deps (torch + sentence-transformers) are optional at runtime.
# On memory-constrained deploys (e.g. Render free tier) they are left out of
# requirements entirely, so we import lazily and guard against absence
# instead of crashing the whole app at import time.
try:
    from sentence_transformers import SentenceTransformer
    _SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    _SENTENCE_TRANSFORMERS_AVAILABLE = False

# Master on/off switch for semantic (embedding-based) matching.
# If false, SEMANTIC_MATCH_ENABLED is always false and semantic_matcher.py
# uses its difflib fallback, regardless of what's installed/configured below.
_SEMANTIC_MATCH_REQUESTED = os.getenv("ENABLE_SEMANTIC_MATCH", "true").lower() == "true"

# Which embedding backend to use:
#   "hf_api" -> call the Hugging Face Inference API over HTTP (no torch needed
#               locally, tiny memory footprint, small network latency/cost)
#   "local"  -> load sentence-transformers in-process (best latency, but
#               needs torch installed + enough RAM)
#   "auto"   -> prefer hf_api if HF_API_KEY is set, else fall back to local
#               if sentence-transformers is installed
EMBEDDING_BACKEND = os.getenv("EMBEDDING_BACKEND", "auto").lower()

HF_API_KEY = os.getenv("HF_API_KEY")
HF_EMBEDDING_MODEL = os.getenv(
    "HF_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
)
HF_API_URL = f"https://api-inference.huggingface.co/models/{HF_EMBEDDING_MODEL}"


def _resolve_backend():
    """
    Decide which embedding backend is actually usable given what's
    installed/configured. Returns "hf_api", "local", or None (meaning:
    no ML backend available - caller should fall back to difflib).
    """

    if EMBEDDING_BACKEND == "hf_api":
        return "hf_api" if HF_API_KEY else None

    if EMBEDDING_BACKEND == "local":
        return "local" if _SENTENCE_TRANSFORMERS_AVAILABLE else None

    # "auto": prefer the Hugging Face API (lightweight), fall back to a
    # local model if one is installed, else no ML backend at all.
    if HF_API_KEY:
        return "hf_api"

    if _SENTENCE_TRANSFORMERS_AVAILABLE:
        return "local"

    return None


_ACTIVE_BACKEND = _resolve_backend() if _SEMANTIC_MATCH_REQUESTED else None

# Read by semantic_matcher.py to decide whether to use ML matching or the
# difflib fallback.
SEMANTIC_MATCH_ENABLED = _ACTIVE_BACKEND is not None


class EmbeddingModel:

    _instance = None
    _model = None  # only populated for the "local" backend

    def __new__(cls):

        if cls._instance is None:

            cls._instance = super().__new__(cls)

        return cls._instance

    def _get_local_model(self):

        if EmbeddingModel._model is None:

            print("Loading local embedding model...")

            EmbeddingModel._model = SentenceTransformer(
                "all-MiniLM-L6-v2"
            )

        return EmbeddingModel._model

    def _encode_via_hf_api(self, texts, retries=3, wait_seconds=3):
        """
        Call the Hugging Face Inference API's feature-extraction endpoint
        to get sentence embeddings, instead of loading the model locally.
        Retries a few times if the model is still "warming up" on HF's side
        (503 response), which is common on the free tier.
        """

        headers = {"Authorization": f"Bearer {HF_API_KEY}"}
        payload = {"inputs": texts, "options": {"wait_for_model": True}}

        last_error = None

        for attempt in range(retries):

            try:
                response = requests.post(
                    HF_API_URL,
                    headers=headers,
                    json=payload,
                    timeout=30
                )

                if response.status_code == 200:

                    embeddings = np.array(response.json())

                    # Normalize rows, matching normalize_embeddings=True
                    # from the local sentence-transformers path.
                    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
                    norms[norms == 0] = 1

                    return embeddings / norms

                if response.status_code == 503:
                    # Model is loading on HF's side - wait and retry.
                    time.sleep(wait_seconds)
                    continue

                last_error = RuntimeError(
                    f"HF Inference API error {response.status_code}: "
                    f"{response.text[:200]}"
                )

            except requests.RequestException as exc:
                last_error = exc
                time.sleep(wait_seconds)

        raise RuntimeError(
            f"HF Inference API call failed after {retries} attempts: "
            f"{last_error}"
        )

    def encode_text(
        self,
        text
    ):

        return self.encode_batch([text])[0]

    def encode_batch(
        self,
        texts
    ):

        if not SEMANTIC_MATCH_ENABLED:
            raise RuntimeError(
                "Semantic matching is disabled: no embedding backend is "
                "available. Set HF_API_KEY to use the Hugging Face "
                "Inference API, or install sentence-transformers for a "
                "local model."
            )

        if _ACTIVE_BACKEND == "hf_api":
            return self._encode_via_hf_api(texts)

        model = self._get_local_model()

        return model.encode(

            texts,

            normalize_embeddings=True
        )