import numpy as np
from fastapi import APIRouter, Depends

from app.middleware.auth import verify_api_key
from app.models.schemas import RetrieveRequest, RetrieveResponse, RetrievedDocument
from app.services.embedding import get_embedding_model
from app.services.language import detect_lang
from app.services.vector_store import get_docstore, search_vectors

router = APIRouter(prefix="", tags=["retrieve"], dependencies=[Depends(verify_api_key)])


@router.post("/retrieve", response_model=RetrieveResponse)
async def retrieve_documents(request: RetrieveRequest) -> RetrieveResponse:
    query_lang = detect_lang(request.query)
    model = get_embedding_model()

    query_vec = model.encode([request.query], normalize_embeddings=True)
    query_vec = np.asarray(query_vec, dtype=np.float32)

    distances, indices = search_vectors(query_vec, request.top_k)
    docstore = get_docstore()

    results: list[RetrievedDocument] = []
    for i, idx in enumerate(indices[0]):
        if idx < 0 or idx >= len(docstore):
            continue
        meta = docstore[idx]
        results.append(
            RetrievedDocument(
                text=meta["text"],
                score=float(distances[0][i]),
                doc_id=meta["doc_id"],
                lang=meta["lang"],
                filename=meta["filename"],
                chunk_id=meta["chunk_id"],
            )
        )

    return RetrieveResponse(query_language=query_lang, results=results)
