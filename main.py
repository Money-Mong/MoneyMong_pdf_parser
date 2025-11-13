import os
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
    # processed, results = run_pipeline()

    # # json으로 저장해서 test
    # for result in results:
    #     doc_to_json = build_document_json(result)
    #     json_path = os.path.join(JSON_DIR, f"{doc_to_json['document_id']}.json")
    #     save_json(doc_to_json, json_path)
    #     store_pipeline_result_to_db(result)
    # return {"status": "completed", "processed_count": len(processed), "processed": processed, "message": "All PDF files processed and stored successfully."}
    return {"status": "completed", "message": "All PDF files processed and stored successfully."}



