
import logging
from fastapi import FastAPI
from dotenv import load_dotenv

logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
load_dotenv()

# FastAPI 앱 생성
app = FastAPI(title="Moneymong PDF Parser", version="1.0.0")

# API 라우터 등록
from app.api.v1.endpoints import router as api_router
app.include_router(api_router)
