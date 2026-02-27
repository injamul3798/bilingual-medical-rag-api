from functools import lru_cache

from fast_langdetect import detect
from transformers import MarianMTModel, MarianTokenizer

TRANSLATION_MODELS = {
    ("ja", "en"): "Helsinki-NLP/opus-mt-ja-en",
    ("en", "ja"): "Helsinki-NLP/opus-mt-en-jap",
}


def detect_lang(text: str) -> str:
    try:
        result = detect(text[:300], low_memory=True)
    except TypeError:
        result = detect(text[:300])

    lang = "en"
    if isinstance(result, dict):
        lang = str(result.get("lang", "en")).lower()
    elif isinstance(result, str):
        lang = result.lower()
    elif isinstance(result, (list, tuple)) and result:
        first = result[0]
        if isinstance(first, dict):
            lang = str(first.get("lang", "en")).lower()
        elif isinstance(first, (list, tuple)) and first:
            lang = str(first[0]).lower()
        elif isinstance(first, str):
            lang = first.lower()

    return "ja" if lang == "ja" else "en"


@lru_cache(maxsize=2)
def _load_translation_pair(src: str, tgt: str):
    model_name = TRANSLATION_MODELS[(src, tgt)]
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    return tokenizer, model


def translate(text: str, src: str, tgt: str) -> str:
    if src == tgt:
        return text
    if (src, tgt) not in TRANSLATION_MODELS:
        raise ValueError(f"Unsupported translation pair: {(src, tgt)}")

    tokenizer, model = _load_translation_pair(src, tgt)
    inputs = tokenizer([text], return_tensors="pt", truncation=True, max_length=512)
    generated = model.generate(**inputs, max_length=512)
    return tokenizer.decode(generated[0], skip_special_tokens=True)
