from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from .api.routes import router
from .config import settings

app = FastAPI(title="AI Chat API", debug=settings.DEBUG)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix=settings.API_PREFIX)