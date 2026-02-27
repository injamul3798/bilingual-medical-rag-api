from app.services.openai_enums import OpenAIModel
from app.services.openai_objects import OpenaiObject

_openai_object = OpenaiObject()


def generate_answer(system_prompt: str, user_message: str) -> str:
    response = _openai_object.create_response_api_call(
        model=OpenAIModel.GPT_4_1_MINI,
        ai_input=[
            _openai_object.format_system_message(system_prompt),
            _openai_object.format_user_message(user_message),
        ],
    )
    return response.output_text
