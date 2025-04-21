from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    """
    Application configuration using Pydantic for type-safe environment variable management.
    """
    DATABASE_URL: str  # PostgreSQL connection URL
    SECRET_KEY: str  # Secret key for JWT signing
    GROQ_API_KEY: str  # API key for Groq AI service
    ALGORITHM: str = "HS256"  # JWT signing algorithm
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # JWT token expiration time

    class Config:
        env_file = ".env"  # Specify .env file for environment variables
        env_file_encoding = "utf-8"

# Instantiate settings object for application-wide use
settings = Settings()