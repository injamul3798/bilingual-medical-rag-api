from typing import Literal

from pydantic import BaseModel, Field


class RetrieveRequest(BaseModel):
    query: str
    top_k: int = Field(default=3, ge=1, le=10)


class RetrievedDocument(BaseModel):
    text: str
    score: float
    doc_id: str
    lang: Literal["en", "ja"]
    filename: str
    chunk_id: int


class IngestResponse(BaseModel):
    doc_id: str
    chunks_ingested: int
    language_detected: Literal["en", "ja"]
    filename: str


class RetrieveResponse(BaseModel):
    query_language: Literal["en", "ja"]
    results: list[RetrievedDocument]


class GenerateRequest(BaseModel):
    query: str
    output_language: Literal["en", "ja"] | None = None
    top_k: int = Field(default=3, ge=1, le=10)


class GenerateResponse(BaseModel):
    answer: str
    query_language: Literal["en", "ja"]
    output_language: Literal["en", "ja"]
    source_documents: list[RetrievedDocument]
