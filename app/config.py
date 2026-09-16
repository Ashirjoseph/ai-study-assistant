from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_ENV: str = "development"

    # Database (used from Phase 2 onward)
    DATABASE_URL: str = "sqlite:///./study_assistant.db"

    # LLM (used from Phase 3 onward)
    LLM_API_KEY: str = ""
    LLM_MODEL: str = "gpt-4o-mini"
    LLM_MAX_TOKENS: int = 400
    LLM_BASE_URL: str | None = None  # override for OpenAI-compatible providers

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
