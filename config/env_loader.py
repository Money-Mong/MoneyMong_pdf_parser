# MoneMong_pdf_parser/config/env_loader.py
import os, sys
from contextlib import contextmanager
from dotenv import dotenv_values

# PDF Parser, BE 각각의 .env 경로
PARSER_ENV = "/Users/jenzennii/Development/moneymong/MoneyMong_pdf_parser/.env"
BE_ENV     = "/Users/jenzennii/Development/moneymong/MoneyMong_BE/.env"

# oneyMong_BE 모듈 패키지 경로 명시
EXPLICIT_PATH = "/Users/jenzennii/Development/moneymong/MoneyMong_BE" 

# parser 환경 우선 로드
parser_env = dotenv_values(PARSER_ENV)
for k, v in parser_env.items():
    if v is not None:
        os.environ[k] = v

# BE 환경의 DB 관련 key만 병합
DB_KEYS = {"POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_DB", "POSTGRES_HOST", "DATABASE_URL"}
if os.path.exists(BE_ENV):
    be_env = dotenv_values(BE_ENV)
    for k in DB_KEYS:
        if k in be_env and be_env[k] is not None:
            os.environ[k] = be_env[k]

# BE 루트 경로 세팅
BE_ROOT = os.environ.get("PYTHONPATH") or EXPLICIT_PATH

@contextmanager
def be_context():
    """ MoneyMong_BE 환경을 임시로 활성화 (모델 import용)"""
    prev = os.getcwd()
    if BE_ROOT not in sys.path:
        sys.path.append(BE_ROOT)
    os.chdir(BE_ROOT)
    try:
        yield
    finally:
        os.chdir(prev)

print("✅ Loaded parser + BE DB environment successfully")
