# MoneMong_pdf_parser/db/db_connector.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from config.env_loader import *                                                 # 환경 로드 (DB_URL 포함)

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL이 환경 변수에 설정되지 않았습니다.")

# SQLAlchemy 엔진 생성
engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)

# 세션팩토리
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """FastAPI 스타일 세션 생성기 (컨텍스트 기반 사용 가능)"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

print("✅ DB 연결 엔진 및 세션팩토리 초기화 완료")
