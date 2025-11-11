import os
from fastapi import FastAPI
from pipeline.run_pipeline import run_pipeline
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
    processed, results = run_pipeline()

    # json으로 저장해서 test
    for result in results:
        doc_to_json = build_document_json(result)
        json_path = os.path.join(JSON_DIR, f"{doc_to_json['report_id']}.json")
        save_json(doc_to_json, json_path)

    return {"status": "completed", "processed_count": len(processed), "processed": processed}



