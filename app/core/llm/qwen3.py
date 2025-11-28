''' 
    [런팟에 vllm 배포했다면]
    python3 -m vllm.entrypoints.openai.api_server \
    --model Qwen/Qwen-VL-Chat \
    --port 8000 \
    --tensor-parallel-size 1 \
    --gpu-memory-utilization 0.9
'''

import os
import requests

QWEN_API_BASE = os.getenv("QWEN_API_BASE", "http://localhost:8000/v1")

def get_qwen_llm(text: str) -> str:
    payload = {
        "model": "Qwen/Qwen-VL-Chat",  # 모델 이름은 실제 배포에 맞게
        "messages": [
            {"role": "system", "content": "문서를 요약해주세요."},
            {"role": "user", "content": text}
        ],
        "temperature": 0.3,
        "max_tokens": 1024
    }

    response = requests.post(
        f"{QWEN_API_BASE}/chat/completions", json=payload
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

