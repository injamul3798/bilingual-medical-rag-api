# Medical RAG Backend (EN/JA)

## Setup

1. Create a virtual environment and activate it.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and set values.
4. Run:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Security

All endpoints require `X-API-Key` header. Valid keys are loaded from `VALID_API_KEYS` in `.env`.

## Endpoints

- `POST /ingest` (multipart/form-data, `file` .txt <= 5MB)
- `POST /retrieve` (`query`, optional `top_k` default 3 max 10)
- `POST /generate` (`query`, optional `output_language`, optional `top_k`)

## Design Notes

- Embeddings use `paraphrase-multilingual-mpnet-base-v2` loaded once at startup.
- FAISS uses `IndexFlatIP(768)` with `faiss.normalize_L2` on add and search.
- Language detection uses `fast-langdetect` and maps output to `en`/`ja`.
- Chunking uses `RecursiveCharacterTextSplitter` with language-specific separators.
- Translation uses MarianMT with lazy-cached model loading.
- Generation uses OpenAI Responses API with `gpt-4.1-mini`.

## Docker

```bash
docker compose up --build
```

## Tests

```bash
pytest tests/ --cov=app --cov-report=xml
```
