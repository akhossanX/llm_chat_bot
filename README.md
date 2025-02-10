# LLM chatbot

A Basic LLM chatbot featuring a React frontend and FastAPI backend, providing a unified interface for multiple LLM providers (Gemini, OpenAI, Anthropic).

## Design Patterns

### Strategy Pattern
- Implemented through the `AIProvider` abstract base class
- Allows switching between different LLM providers seamlessly
- Each provider implements the same interface for consistency

### Factory Pattern
- `AIProviderFactory` creates appropriate provider instances
- Providers can be switched via environment variables
- Simplifies adding new providers

## Local Development

### Backend Setup

1. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
# Create .env file
cp .env.example .env

# Add your API keys
GEMINI_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
```

3. Run the development server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Run the development server:
```bash
npm run dev
```

The frontend will be available at http://localhost:3000

## Docker Setup

Build and run both services using Docker Compose:
```bash
docker-compose up
```

This will:
- Build and start both frontend and backend services
- Mount code directories for live reloading
- Start the frontend on port 3000 and backend on port 8000

## API Endpoints

### Chat Endpoint
```
POST /api/chat
```

Request body:
```json
{
    "message": "Your message here"
}
```

Response:
```json
{
    "response": "AI generated response",
    "timestamp": "2024-02-10T12:00:00Z",
    "provider": "gemini"
}
```

## Provider Implementation

To implement a new AI provider:

1. Create a new service class inheriting from `AIProvider`:
```python
from .base import AIProvider

class NewProvider(AIProvider):
    async def generate_response(self, message: str) -> str:
        # Implementation here
        pass

    async def get_model_info(self) -> Dict[str, Any]:
        # Implementation here
        pass
```

2. Add the provider to the factory:
```python
class AIProviderFactory:
    _providers = {
        "new_provider": NewProvider,
        # ... other providers
    }
```

## Environment Configuration

```bash
# General settings
DEBUG=1
ENVIRONMENT=development

# Provider selection
AI_PROVIDER=gemini  # Options: gemini, openai, anthropic

# API Keys
GEMINI_API_KEY=your_key
OPENAI_API_KEY=your_key
ANTHROPIC_API_KEY=your_key
```

## Error Handling

The service implements comprehensive error handling:
- API-specific errors (rate limits, quotas)
- Network errors
- Invalid input validation
- Service unavailability

Example error response:
```json
{
    "detail": "Error message here",
    "error_code": "PROVIDER_ERROR",
    "timestamp": "2024-02-10T12:00:00Z"
}
```

## Author

Built by [@abdelilah.khossan@gmail.com](mailto:abdelilah.khossan@gmail.com)