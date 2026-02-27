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

##Results Demo
1. Retrive API input and output
   <img width="975" height="441" alt="image" src="https://github.com/user-attachments/assets/977f56d4-fd91-4e92-9d67-f5309f70d3e0" />
   <img width="975" height="443" alt="image" src="https://github.com/user-attachments/assets/c0a1afe5-818a-4bc0-899a-72961cbadce8" />

2. Genration API input and output
   <img width="975" height="402" alt="image" src="https://github.com/user-attachments/assets/3201802b-a276-4885-b933-7b45e4ad12d9" />
   <img width="975" height="400" alt="image" src="https://github.com/user-attachments/assets/4c2abca4-2f71-4a3c-8848-4bafa5a5a573" />


   
