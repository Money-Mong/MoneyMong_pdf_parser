# pdf-parser
- [x] PDF에서 텍스트, 테이블 이미지 분류해서 데이터 저장
- [x] 텍스트 데이터에 대한 청킹, 임베딩 수행 (*현재 UpstageAPI를 사용, 추후 openAI로 변경 예정)
- [x] DB구조에 맞게 반환값 설정
- [x] 임베딩 벡터 DB에 저장 (pgvector, sqlalchemy)

------
## 실행 전 주의사항
- .env파일 개별 설정 수행
- 가상환경 구성 후 requirements.txt 로 필요한 패키지 설치

## run
```uvicorn main:app --host 0.0.0.0 --port 8000 ```</br>
```http://0.0.0.0:8000/docs``` 주소로 진입

## 디렉토리 구조 및 모듈 설명(v1.1.0)
```
moneymong_pdf_parser/
├── Dockerfile
├── init.sh
├── requirements.txt
│
├── main.py                          # FastAPI 엔트리 포인트 (원격 실행)
├── run_pipeline_parallel.py         # 병렬 처리 기반 전체 파이프라인 실행
│
├── app/
│   ├── routes/						# FastAPI 라우터
│   │   └── pdf_parser.py
│   └── services/					# FastAPI 서비스
│       └── pdf_pipeline.py
├── config/
│   ├── __init__.py
│   ├── env_loader.py                # 환경 변수 관리 (.env)
│   └── paths.py                     # 경로 설정
├── db/
│   ├── __init__.py
│   ├── db_connector.py              # db 연결
│   └── insert_asset.py              # asset 레코드 
│   └── insert_layout.py             # layout 레코드 
│   └── insert_chunk.py              # chunk 레코드 
│   └── insert_document.py           # 문서 갱신 (pending->completed)
│   └── insert_pipeline.py           # 레코드 삽입
│
├── layout/
│   ├── __init__.py
|	├── detect_table_crop.py         # 레이아웃 label중 table만 crop해서 이미지로 저장
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
│   ├── pipeline_parser.py           # 문서 데이터 처리 파이프라인
│   └── pipeline_db_store.py         # db에 데이터 저장 파이프라인
│   └── document_to_json.py          # pdf 처리 결과 json 구조(출력확인용)
│
└── utils/
		├── deter_loader.py              # detr 모델 로드해서 import로 처리하기 위함
    ├── logger.py                    # 로그 포맷팅
    ├── file_utils.py                # 파일 I/O (S3 또는 로컬)
    └── time_tracker.py              # 처리 시간 측정 유틸

```
