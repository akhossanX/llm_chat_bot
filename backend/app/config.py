from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # General settings
    API_PREFIX: str = "/api"
    DEBUG: bool = False

    # Server settings
    HOST: str = "0.0.0.0"  # Add this
    PORT: int = 8000       # Add this

    # AI Provider settings
    AI_PROVIDER: str = "gemini"  # or "anthropic" or others
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    GEMINI_API_KEY: str = ""


    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()