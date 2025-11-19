import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
from fastapi import FastAPI
from pipeline.pipeline_db_store import run_db_store_pipeline
from utils.file_io import save_json
from dotenv import load_dotenv
from config.paths import JSON_DIR

# FastAPI 시작 시 .env 자동 로드
load_dotenv()
app = FastAPI(title="Moneymong S3 PDF Pipeline", version="1.0.0")

@app.get("/")
def root():
    return {"status": "ok", "message": "Moneymong S3 PDF Pipeline"}

@app.post("/pdf-parser")
def run_task():
    run_db_store_pipeline()

    return {"status": "completed", "message": "All PDF files processed and stored successfully."}

@app.post("/ner-backfill")
def ner_backfill_task():
    """
    기존에 DB에 쌓인 documents & document_chunks에 대해
    NER 기반 metadata / keywords를 채워 넣는 백필 작업
    """
    from scripts.ner_backfill import run_ner_backfill
    run_ner_backfill()
    return {
        "status": "completed",
        "message": "NER backfill executed successfully.",
    }