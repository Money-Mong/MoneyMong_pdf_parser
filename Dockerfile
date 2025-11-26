FROM python:3.10

# 모델 캐시 경로 설정
ENV HF_HOME=/workspace/cache/model
ENV TOKENIZERS_PARALLELISM=false

# 작업 디렉토리 설정
WORKDIR /app
ENV PYTHONPATH="/app"

# 현재 디렉토리 모든 파일 복사
COPY . /app

# pip 업그레이드 및 의존성 설치
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# FastAPI를 실행하던 경우 아래 명령어를 사용했었음
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000"]

# 서버리스 환경에서는 엔트리포인트 함수 실행
CMD ["python3", "-u", "/app/entrypoint.py"]
