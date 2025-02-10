from typing import Dict, Any
import anthropic

from .base import AIProvider
from ..config import settings

from fastapi import HTTPException


class AnthropicProvider(AIProvider):
    """
    Anthropic AI service provider implementation using Claude.
    This class handles all interactions with the Anthropic API,
    including proper error handling and response formatting.
    """

    def __init__(self):
        """
        Initialize the Anthropic client with API key and default model.
        We use Claude 3 Sonnet as the default model since it offers a good
        balance of capability and speed.
        """
        try:
            self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
            # Default to Claude 3 Sonnet, but this could be configurable
            self.model = "claude-3-sonnet-20240229"
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to initialize Anthropic client: {str(e)}"
            )

    async def generate_response(self, message: str) -> str:
        """
        Generate a response using the Anthropic API.

        Args:
            message (str): The user's input message

        Returns:
            str: The generated response from Claude

        Raises:
            HTTPException: If there's an error calling the API or processing the response
        """
        try:
            # Create a message with system prompt if needed
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,  # Adjustable based on your needs
                messages=[
                    {
                        "role": "user",
                        "content": message
                    }
                ],
                temperature=0.7  # Adjustable based on desired creativity level
            )

            # Extract the response content
            if response.content:
                return response.content[0].text
            else:
                raise HTTPException(
                    status_code=500,
                    detail="Empty response from Anthropic API"
                )

        except anthropic.APIError as e:
            # Handle rate limits and API-specific errors
            if e.status_code == 429:
                raise HTTPException(
                    status_code=429,
                    detail="Rate limit exceeded. Please try again later."
                )
            raise HTTPException(
                status_code=500,
                detail=f"Anthropic API error: {str(e)}"
            )
        except anthropic.APIConnectionError as e:
            # Handle network and connection errors
            raise HTTPException(
                status_code=503,
                detail="Failed to connect to Anthropic API. Please try again later."
            )
        except Exception as e:
            # Handle any unexpected errors
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected error: {str(e)}"
            )

    async def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the current model configuration.
        This is useful for monitoring and debugging purposes.

        Returns:
            Dict[str, Any]: Information about the current model configuration
        """
        return {
            "provider": "anthropic",
            "model": self.model,
            "capabilities": [
                "chat",
                "text_generation",
                "analysis"
            ]
        }