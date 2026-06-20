from backend.models.embedding_model import (
    EmbeddingModel
)

model = EmbeddingModel()

embedding = model.encode_text(
    "Machine Learning"
)

print(
    embedding.shape
)