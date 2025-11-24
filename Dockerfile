FROM python:3.10

# 모델 캐시 경로 설정
ENV TRANSFORMERS_CACHE=/workspace/cache/model
ENV TOKENIZERS_PARALLELISM=false

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# EXPOSE 3000

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000"]
CMD ["python", "entrypoint.py"]