import os
# from dotenv import load_dotenv
from app.config.settings import get_settings
from app.core.llm.upstage import get_upstage_llm
from app.core.llm.qwen3 import get_qwen_llm


settings = get_settings()

def get_summary_llm():
    if settings.USE_QWEN3:
        return get_qwen_llm()
    elif settings.USE_UPSTAGE:
        return get_upstage_llm()
    else:
        raise ValueError("❌ 사용할 LLM 설정이 없습니다. .env에서 USE_QWEN3 or USE_UPSTAGE 설정 확인")

