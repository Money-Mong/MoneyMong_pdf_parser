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
MoneyMong_pdf_parser/
├── .env
├── Dockerfile
├── init.sh
├── README.md
├── requirements.txt
├── scripts/
│   └── run_pipeline_parallel.py
└── app/
    ├── __init__.py
    ├── main.py
    ├── api/
    │   ├── __init__.py
    │   └── v1/
    │       ├── __init__.py
    │       └── endpoints.py         
    ├── config/
    │   ├── __init__.py
    │   ├── env_loader.py
    │   └── paths.py
    ├── core/
    │   ├── __init__.py
    │   ├── layout/
    │   │   ├── __init__.py
    │   │   ├── detect_layout.py
    │   │   ├── detect_table_crop.py
    │   │   └── save_page.py
    │   ├── llm/
    │   │   ├── __init__.py
    │   │   ├── prompts.py
    │   │   └── summary.py
    │   └── text/
    │       ├── __init__.py
    │       ├── embedding.py
    │       ├── ner.py
    │       ├── ner_utils.py
    │       ├── pdfminer_extractor.py
    │       └── text_cleaner.py
    ├── db/
    │   ├── __init__.py
    │   ├── db_connector.py
    │   ├── insert_asset.py
    │   ├── insert_chunk.py
    │   ├── insert_document.py
    │   ├── insert_layout.py
    │   ├── insert_pipeline.py
    │   ├── insert_summary.py
    │   ├── queries.py
    ├── resource/
    │   └── KRX_company.csv
    ├── services/
    │   ├── __init__.py
    │   ├── ner_backfill.py
    │   ├── summary_update.py      
    │   └── pipeline/
    └── utils/
        ├── __init__.py
        ├── detr_loader.py
        ├── file_io.py
        ├── file_loader.py
        ├── logger.py
        ├── ner_loader.py
        ├── sanitize.py
        └── time_tracker.py

```
