
from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "MoneyMong API"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False

    # aws
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str = "ap-northeast-2"

    # s3
    S3_BUCKET: str = "moneymong-resources-bucket"
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

# # MoneMong_pdf_parser/config/env_loader.py
# import os, sys
# from contextlib import contextmanager
# from dotenv import dotenv_values

# # (로컬)PDF Parser, BE 각각의 .env 경로 명시
# PARSER_ENV = "/Users/jenzennii/Development/moneymong/MoneyMong_pdf_parser/.env"
# BE_ENV     = "/Users/jenzennii/Development/moneymong/MoneyMong_BE/.env"

# # (로컬)oneyMong_BE 모듈 패키지 경로 명시
# EXPLICIT_PATH = "/Users/jenzennii/Development/moneymong/MoneyMong_BE" 

# # parser 환경 우선 로드
# parser_env = dotenv_values(PARSER_ENV)
# for k, v in parser_env.items():
#     if v is not None:
#         os.environ[k] = v

# # BE 환경의 DB 관련 key만 병합
# DB_KEYS = {"POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_DB", "POSTGRES_HOST", "DATABASE_URL"}
# if os.path.exists(BE_ENV):
#     be_env = dotenv_values(BE_ENV)
#     for k in DB_KEYS:
#         if k in be_env and be_env[k] is not None:
#             os.environ[k] = be_env[k]

# # BE 루트 경로 세팅
# BE_ROOT = os.environ.get("PYTHONPATH") or EXPLICIT_PATH

# @contextmanager
# def be_context():
#     """ MoneyMong_BE 환경을 임시로 활성화 (모델 import용)"""
#     prev = os.getcwd()
#     if BE_ROOT not in sys.path:
#         sys.path.insert(0, BE_ROOT)
#     os.chdir(BE_ROOT)
#     try:
#         yield
#     finally:
#         os.chdir(prev)

# print("✅ Loaded parser + BE DB environment successfully")
