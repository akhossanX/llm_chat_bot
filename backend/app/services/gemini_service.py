# services/gemini_service.py

import google.generativeai as genai
from typing import Dict, Any
from fastapi import HTTPException
from .base import AIProvider
from ..config import settings


class GeminiProvider(AIProvider):
    """
    Google's Gemini AI service provider implementation.
    This class handles interactions with the Gemini API, providing a reliable
    and efficient way to generate responses while handling errors appropriately.
    """

    def __init__(self):
        """
        Initialize the Gemini client with API key and configure default settings.
        Gemini Pro is currently the most capable model available through the API.
        """
        try:
            # Configure the Gemini API with your key
            genai.configure(api_key=settings.GEMINI_API_KEY)

            # Initialize the model - Gemini-Pro is the default conversation model
            self.model = genai.GenerativeModel('gemini-pro')

            # Start a chat session - this helps maintain conversation context
            self.chat = self.model.start_chat(history=[])

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to initialize Gemini client: {str(e)}"
            )

    async def generate_response(self, message: str) -> str:
        """
        Generate a response using the Gemini API.

        The method includes safety checks and error handling to ensure
        reliable operation even when facing API issues.

        Args:
            message (str): The user's input message

        Returns:
            str: The generated response from Gemini

        Raises:
            HTTPException: If there's an error calling the API or processing the response
        """
        try:
            # Generate the response
            response = self.chat.send_message(
                message,
                generation_config={
                    'temperature': 0.7,  # Controls response creativity
                    'top_p': 0.8,  # Nucleus sampling parameter
                    'top_k': 40,  # Top-k sampling parameter
                    'max_output_tokens': 2048,  # Maximum length of the response
                }
            )

            # Extract the response text
            if response.text:
                return response.text
            else:
                raise HTTPException(
                    status_code=500,
                    detail="Empty response from Gemini API"
                )

        except Exception as e:
            # Handle various types of errors that might occur
            error_message = str(e)

            if "quota exceeded" in error_message.lower():
                raise HTTPException(
                    status_code=429,
                    detail="Rate limit exceeded. Please try again later."
                )
            elif "invalid api key" in error_message.lower():
                raise HTTPException(
                    status_code=401,
                    detail="Invalid API key. Please check your configuration."
                )
            else:
                raise HTTPException(
                    status_code=500,
                    detail=f"Gemini API error: {error_message}"
                )

    async def get_model_info(self) -> Dict[str, Any]:
        """
        Provide information about the current model configuration.
        This is useful for monitoring and debugging purposes.

        Returns:
            Dict[str, Any]: Information about the current model and its capabilities
        """
        return {
            "provider": "gemini",
            "model": "gemini-pro",
            "capabilities": [
                "chat",
                "text_generation",
                "analysis",
                "code_generation"
            ]
        }