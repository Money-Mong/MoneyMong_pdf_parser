import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
from fastapi import FastAPI
from pipeline.pipeline_parser import run_pdf_pipeline
from pipeline.pipeline_db_store import run_db_store_pipeline
from pipeline.document_to_json import build_document_json
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

