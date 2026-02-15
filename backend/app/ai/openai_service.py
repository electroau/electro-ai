from openai import AsyncOpenAI

from app.core.config import get_settings

settings = get_settings()
client = AsyncOpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None


async def ask_assistant(prompt: str) -> str:
    if client is None:
        return "OpenAI API key is not configured."
    response = await client.responses.create(
        model=settings.openai_model,
        input=prompt,
    )
    return response.output_text
