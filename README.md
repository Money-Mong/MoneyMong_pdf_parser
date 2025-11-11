
## 실행 전 주의사항
- .env파일 개별 설정 수행
- 가상환경 구성 후 requirements.txt 로 필요한 패키지 설치

## run
```uvicorn main:app --host 0.0.0.0 --port 8000 ```</br>
```http://0.0.0.0:8000/docs``` 주소로 진입

## 디렉토리 구조 및 모듈 설명(v1.0.0)
```
moneymong_pdf_parser/
├── Dockerfile
├── init.sh
├── requirements.txt
│
├── main.py                          # FastAPI 엔트리 포인트 (원격 실행)
├── run_pipeline_parallel.py         # 병렬 처리 기반 전체 파이프라인 실행
│
├── config/
│   ├── __init__.py
│   ├── env_loader.py                # 환경 변수 관리 (.env)
│   └── paths.py                     # 경로 설정
│
├── layout/
│   ├── __init__.py
|		├── detect_table_crop.py         # 레이아웃 label중 table만 crop해서 이미지로 저장
│   ├── detect_layout.py             # DETR 기반 레이아웃 타입감지->PDF 레이아웃 분석 결과
│   └── save_page.py                 # PDF → 이미지 (1p 변환)
│
├── text/
│   ├── __init__.py
│   ├── pdfminer_extractor.py        # PDFMiner 텍스트 추출 (비텍스트 제외)
│   ├── text_cleaner.py              # 문단 정제/개행 처리
│   └── embedding.py                 # GPT-4o mini Embedding (LangChain)
│
├── pipeline/
│   ├── __init__.py
│   ├── run_pipeline.py              # 단일 문서 파이프라인
│   └── utils_parallel.py            # 멀티프로세싱 관리 로직(미구성)
│   └── document_to_json.py          # pdf 처리 결과 json 구조(출력확인용)
│
└── utils/
		├── deter_loader.py              # detr 모델 로드해서 import로 처리하기 위함
    ├── logger.py                    # 로그 포맷팅
    ├── file_utils.py                # 파일 I/O (S3 또는 로컬)
    └── time_tracker.py              # 처리 시간 측정 유틸

```
