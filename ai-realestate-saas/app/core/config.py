import os
from dotenv import load_dotenv

load_dotenv()

class Settings:

    PROJECT_NAME: str = "AI Real Estate SaaS Engine"

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./app.db"
    )

    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "groq")

    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")

    AI_MODEL: str = os.getenv(
        "AI_MODEL",
        "openai/gpt-oss-20b"
    )

    SECRET_KEY: str = os.getenv(
        "SECRET_KEY",
        "change-this-in-production"
    )

    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7


settings = Settings()