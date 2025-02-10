from typing import Dict, Any

from openai import AsyncOpenAI

from ..config import settings
from .base import AIProvider


class OpenAIProvider(AIProvider):

    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = "gpt-3.5-turbo"

    async def generate_response(self, message: str) -> str:
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": message}]
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")

    async def get_model_info(self) -> Dict[str, Any]:
        """
        Implements the abstract get_model_info method to provide information
        about the current OpenAI model configuration.
        """
        return {
            "provider": "openai",
            "model": self.model,
            "capabilities": {
                "streaming": True,
                "function_calling": True,
                "max_tokens": 4096
            }
        }