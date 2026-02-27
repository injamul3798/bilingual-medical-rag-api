from sentence_transformers import SentenceTransformer

from app.config import get_settings

_model: SentenceTransformer | None = None


def load_embedding_model() -> SentenceTransformer:
    global _model
    if _model is None:
        settings = get_settings()
        _model = SentenceTransformer(settings.MODEL_NAME)
    return _model


def get_embedding_model() -> SentenceTransformer:
    if _model is None:
        raise RuntimeError("Embedding model is not loaded")
    return _model
