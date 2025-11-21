
from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "MoneyMong API"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    
    # llm select
    USE_QWEN3: bool = False
    USE_UPSTAGE: bool = False
    QWEN_API_BASE: str
    # aws
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str

    # s3
    S3_BUCKET: str 
    USE_S3: bool = True
    S3_RAW_PREFIX: str
    S3_CROP_PREFIX: str
    S3_PAGE_IMG_PREFIX: str

    # OpenAI
    OPENAI_API_KEY: str

    # HuggingFace
    HF_API_KEY: str

    # Upstage
    UPSTAGE_API_KEY: str

    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:3000",        # FastAPI Docs 테스트용
    ]
    
    # API
    API_HOST: str = "localhost"
    API_PORT: int = 8000
    RELOAD: bool = True

    # DB
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432  # 타입 힌트와 기본값 활용
    DATABASE_URL: str


    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = 'allow'

@lru_cache()
def get_settings() -> Settings:
    return Settings()