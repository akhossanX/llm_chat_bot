from typing import Dict, Type

from .base import AIProvider
from .anthropic_service import AnthropicProvider
from .gemini_service import GeminiProvider
from .openai_service import OpenAIProvider


class AIProviderFactory:
    _providers: Dict[str, Type[AIProvider]] = {
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider,
        "gemini": GeminiProvider,
    }

    @classmethod
    def create_provider(cls, provider_name: str) -> AIProvider:
        provider_class = cls._providers.get(provider_name)
        if not provider_class:
            raise ValueError(f"Unknown provider: {provider_name}")
        return provider_class()