from openai import OpenAI
from fastapi import HTTPException

from app.core.config import settings
from app.ai.prompts import SYSTEM_PROMPT
from app.utils.logger import logger


client = OpenAI(
    api_key=settings.GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)


def ask_ai(message: str) -> str:

    try:

        response = client.responses.create(
            model=settings.AI_MODEL,
            input=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            timeout=30
        )

        return response.output_text

    except Exception as e:

        logger.error(f"AI Error: {str(e)}")

        raise HTTPException(
            status_code=503,
            detail="AI service unavailable"
        )