# ✅ GPU 사용을 위한 CUDA 지원 이미지
FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

# Python 설치
RUN apt-get update && \
    apt-get install -y python3.10 python3-pip && \
    ln -s /usr/bin/python3.10 /usr/bin/python && \
    ln -s /usr/bin/pip3 /usr/bin/pip

# 모델 캐시 경로 설정
ENV TRANSFORMERS_CACHE=/workspace/cache/model
ENV TOKENIZERS_PARALLELISM=false

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 3000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000"]
