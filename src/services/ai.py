import google.generativeai as genai

from src.config.dependencies import get_settings


settings = get_settings()


async def get_summarize_note_genai(content: str):
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = await model.generate_content_async(content)

    return response
