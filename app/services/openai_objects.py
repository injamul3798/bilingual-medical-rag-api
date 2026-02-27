from openai import OpenAI

from app.config import get_settings
from app.services.openai_enums import OpenAIModel


class OpenaiObject:
    def __init__(self) -> None:
        self.client: OpenAI | None = None

    def init_client(self) -> None:
        settings = get_settings()
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def format_system_message(self, instruction_text: str) -> dict:
        return {
            "role": "system",
            "content": [{"type": "input_text", "text": instruction_text}],
        }

    def format_user_message(self, message_text: str) -> dict:
        return {
            "role": "user",
            "content": [{"type": "input_text", "text": message_text}],
        }

    def create_response_api_call(self, model: OpenAIModel, ai_input: list[dict]):
        if self.client is None:
            self.init_client()
        return self.client.responses.create(
            model=model.value,
            input=ai_input,
            max_output_tokens=800,
            temperature=0.2,
        )
