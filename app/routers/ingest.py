import uuid

import numpy as np
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.middleware.auth import verify_api_key
from app.models.schemas import IngestResponse
from app.services.embedding import get_embedding_model
from app.services.language import detect_lang
from app.services.vector_store import add_vectors, persist_store

router = APIRouter(prefix="", tags=["ingest"], dependencies=[Depends(verify_api_key)])

MAX_FILE_SIZE = 5 * 1024 * 1024


@router.post("/ingest", response_model=IngestResponse)
async def ingest_document(file: UploadFile = File(...)) -> IngestResponse:
    if not file.filename or not file.filename.lower().endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only .txt files are supported")

    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File size must be <= 5MB")

    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise HTTPException(status_code=400, detail="File must be UTF-8 encoded") from exc

    lang = detect_lang(text)

    separators = ["。", "！", "？", "\n\n", "\n", ""] if lang == "ja" else ["\n\n", "\n", ". ", "! ", "? ", " ", ""]
    splitter = RecursiveCharacterTextSplitter(
        separators=separators,
        chunk_size=512,
        chunk_overlap=77,
    )
    chunks = splitter.split_text(text)
    if not chunks:
        raise HTTPException(status_code=400, detail="No text chunks generated")

    model = get_embedding_model()
    vectors = model.encode(chunks, batch_size=32, normalize_embeddings=True)
    vectors = np.asarray(vectors, dtype=np.float32)

    doc_id = str(uuid.uuid4())
    metadata = [
        {
            "doc_id": doc_id,
            "chunk_id": i,
            "text": chunk,
            "lang": lang,
            "filename": file.filename,
        }
        for i, chunk in enumerate(chunks)
    ]

    add_vectors(vectors, metadata)
    persist_store()

    return IngestResponse(
        doc_id=doc_id,
        chunks_ingested=len(chunks),
        language_detected=lang,
        filename=file.filename,
    )
