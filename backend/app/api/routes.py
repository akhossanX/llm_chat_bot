from fastapi import APIRouter, HTTPException
from datetime import datetime

from ..models.chat import ChatRequest, ChatResponse
from ..services.factory import AIProviderFactory
from ..config import settings

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    try:
        provider = AIProviderFactory.create_provider(settings.AI_PROVIDER)
        response = await provider.generate_response(request.message)

        return ChatResponse(
            response=response,
            timestamp=datetime.utcnow(),
            provider=settings.AI_PROVIDER
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))