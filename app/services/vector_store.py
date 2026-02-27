import json
import os
from threading import Lock
from typing import Any

import faiss
import numpy as np

from app.config import get_settings

INDEX_DIM = 768

_index = faiss.IndexFlatIP(INDEX_DIM)
_docstore: list[dict[str, Any]] = []
_store_lock = Lock()


def initialize_store() -> None:
    global _index, _docstore
    settings = get_settings()
    os.makedirs(os.path.dirname(settings.FAISS_INDEX_PATH), exist_ok=True)

    if os.path.exists(settings.FAISS_INDEX_PATH):
        try:
            _index = faiss.read_index(settings.FAISS_INDEX_PATH)
        except RuntimeError:
            _index = faiss.IndexFlatIP(INDEX_DIM)
    else:
        _index = faiss.IndexFlatIP(INDEX_DIM)

    if os.path.exists(settings.DOCSTORE_PATH):
        try:
            with open(settings.DOCSTORE_PATH, "r", encoding="utf-8-sig") as f:
                data = json.load(f)
                _docstore = data if isinstance(data, list) else []
        except (json.JSONDecodeError, OSError):
            _docstore = []
    else:
        _docstore = []


def get_index() -> faiss.IndexFlatIP:
    return _index


def get_docstore() -> list[dict[str, Any]]:
    return _docstore


def add_vectors(vectors: np.ndarray, metadata: list[dict[str, Any]]) -> None:
    global _docstore
    with _store_lock:
        faiss.normalize_L2(vectors)
        _index.add(vectors)
        _docstore.extend(metadata)


def search_vectors(query_vec: np.ndarray, top_k: int) -> tuple[np.ndarray, np.ndarray]:
    faiss.normalize_L2(query_vec)
    return _index.search(query_vec, top_k)


def persist_store() -> None:
    settings = get_settings()
    with _store_lock:
        faiss.write_index(_index, settings.FAISS_INDEX_PATH)
        with open(settings.DOCSTORE_PATH, "w", encoding="utf-8") as f:
            json.dump(_docstore, f, ensure_ascii=False)
