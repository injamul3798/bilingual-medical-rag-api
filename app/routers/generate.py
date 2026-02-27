from fastapi import APIRouter, Depends, HTTPException
from app.middleware.auth import verify_api_key
from app.models.schemas import GenerateRequest, GenerateResponse
from app.routers.retrieve import retrieve_documents
from app.models.schemas import RetrieveRequest
from app.services.generator import generate_answer
from app.services.generator_free import generate_answer_free
from app.services.language import detect_lang_code, translate
from app.services.prompt import ENGLISH_SYSTEM_PROMPT, JAPANESE_SYSTEM_PROMPT

router = APIRouter(prefix="", tags=["generate"], dependencies=[Depends(verify_api_key)])

UNSUPPORTED_LANG_MSG = "Supported languages are English and Japanese. Please provide input in English or Japanese."


@router.post("/generate", response_model=GenerateResponse)
async def generate_response(request: GenerateRequest) -> GenerateResponse:
    detected = detect_lang_code(request.query)
    if detected not in {"en", "ja"}:
        raise HTTPException(status_code=400, detail=UNSUPPORTED_LANG_MSG)
    query_lang = detected
    output_language = request.output_language or query_lang

    retrieved = await retrieve_documents(RetrieveRequest(query=request.query, top_k=request.top_k))

    context = "\n---\n".join([doc.text for doc in retrieved.results])

    system_prompt = ENGLISH_SYSTEM_PROMPT if output_language == "en" else JAPANESE_SYSTEM_PROMPT

    answer_lang_instruction = "Japanese (日本語)" if output_language == "ja" else "English"
    user_message = (
        f"Medical Documents:\n{context}\n\n"
        f"Question: {request.query}\n\n"
        f"Answer in {answer_lang_instruction}:"
    )

    answer = generate_answer(system_prompt, user_message)

    if output_language != query_lang:
        answer = translate(answer, src=query_lang, tgt=output_language)

    return GenerateResponse(
        answer=answer,
        query_language=query_lang,
        output_language=output_language,
        source_documents=retrieved.results,
    )


@router.post("/generate-free", response_model=GenerateResponse)
async def generate_response_free(request: GenerateRequest) -> GenerateResponse:
    detected = detect_lang_code(request.query)
    if detected not in {"en", "ja"}:
        raise HTTPException(status_code=400, detail=UNSUPPORTED_LANG_MSG)
    query_lang = detected
    output_language = request.output_language or query_lang

    retrieved = await retrieve_documents(RetrieveRequest(query=request.query, top_k=request.top_k))

    context = "\n---\n".join([doc.text for doc in retrieved.results])

    system_prompt = ENGLISH_SYSTEM_PROMPT if output_language == "en" else JAPANESE_SYSTEM_PROMPT

    answer_lang_instruction = "Japanese (日本語)" if output_language == "ja" else "English"
    user_message = (
        f"Medical Documents:\n{context}\n\n"
        f"Question: {request.query}\n\n"
        f"Answer in {answer_lang_instruction}:"
    )

    answer = generate_answer_free(system_prompt, user_message)

    if output_language != query_lang:
        answer = translate(answer, src=query_lang, tgt=output_language)

    return GenerateResponse(
        answer=answer,
        query_language=query_lang,
        output_language=output_language,
        source_documents=retrieved.results,
    )
