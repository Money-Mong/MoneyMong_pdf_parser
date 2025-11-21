FROM python:3.10

# 모델 캐싱 경로
ENV TRANSFORMERS_CACHE=/workspace/cache/model

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 3000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000"]
