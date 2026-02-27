import json
from pathlib import Path

import faiss
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services import embedding, generator, language
from app.services import vector_store


class DummyEmbeddingModel:
    def encode(self, texts, batch_size=32, normalize_embeddings=True):
        if isinstance(texts, str):
            texts = [texts]
        vectors = []
        for i, text in enumerate(texts):
            base = float((len(text) % 10) + 1 + i)
            vec = [0.0] * 768
            vec[0] = base
            vec[1] = base / 2
            vectors.append(vec)
        return vectors


@pytest.fixture(autouse=True)
def setup_env(tmp_path, monkeypatch):
    faiss_path = tmp_path / "index.faiss"
    docstore_path = tmp_path / "docstore.json"

    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("VALID_API_KEYS", "key1,key2")
    monkeypatch.setenv("FAISS_INDEX_PATH", str(faiss_path))
    monkeypatch.setenv("DOCSTORE_PATH", str(docstore_path))
    monkeypatch.setenv("MODEL_NAME", "paraphrase-multilingual-mpnet-base-v2")

    from app.config import get_settings

    get_settings.cache_clear()

    embedding._model = DummyEmbeddingModel()
    vector_store._index = faiss.IndexFlatIP(768)
    vector_store._docstore = []
    vector_store.initialize_store()

    if not Path(docstore_path).exists():
        with open(docstore_path, "w", encoding="utf-8") as f:
            json.dump([], f)


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(language, "detect_lang", lambda text: "ja" if any("\u3040" <= c <= "\u30ff" for c in text) else "en")
    monkeypatch.setattr(generator, "generate_answer", lambda system_prompt, user_message: "Mocked answer")

    def no_translate(text: str, src: str, tgt: str) -> str:
        return f"{text} ({src}->{tgt})" if src != tgt else text

    monkeypatch.setattr(language, "translate", no_translate)

    return TestClient(app)


@pytest.fixture
def auth_headers():
    return {"X-API-Key": "key1"}
