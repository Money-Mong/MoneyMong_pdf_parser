import os
from fastapi import FastAPI
from dotenv import load_dotenv

# 환경 설정
os.environ["TOKENIZERS_PARALLELISM"] = "false"
load_dotenv()

# FastAPI 앱 생성
app = FastAPI(title="Moneymong PDF Parser", version="1.0.0")

# API 라우터 등록
from app.api.v1.endpoints import router as api_router
app.include_router(api_router)
