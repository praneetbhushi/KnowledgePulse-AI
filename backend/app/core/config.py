from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)

class Settings(BaseSettings):

    PROJECT_NAME: str
    VERSION: str
    API_V1_STR: str

    HOST: str
    PORT: int
    DEBUG: bool

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    DATABASE_URL: str

    # Ollama Local LLM
    OLLAMA_MODEL: str = "llama3.2:3b"
    OLLAMA_HOST: str = "http://localhost:11434"

    # Gemini API
    GEMINI_API_KEY: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


settings = Settings()