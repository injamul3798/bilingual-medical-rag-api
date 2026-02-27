from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.routers.generate import router as generate_router
from app.routers.ingest import router as ingest_router
from app.routers.retrieve import router as retrieve_router
from app.services.embedding import load_embedding_model
from app.services.vector_store import initialize_store


@asynccontextmanager
async def lifespan(_: FastAPI):
    load_embedding_model()
    initialize_store()
    yield


app = FastAPI(title="Medical RAG API", lifespan=lifespan)
app.include_router(ingest_router)
app.include_router(retrieve_router)
app.include_router(generate_router)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
