import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
from fastapi import FastAPI
from pipeline.pipeline_db_store import run_db_store_pipeline
from dotenv import load_dotenv
from config.paths import JSON_DIR
from tqdm import tqdm

load_dotenv()

app = FastAPI(title="Moneymong S3 PDF Pipeline", version="1.0.0")

@app.get("/")
def root():
    return {"status": "ok", "message": "Moneymong S3 PDF Pipeline"}


@app.post("/pdf-processing")
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

@app.post("/update-summary-all")
def update_summary_all():
    """
    기존에 DB에 쌓인 documents 에 대해
    document_summary 채워 넣는 백필 작업
    """
    from summary.update_summary import update_all_summaries
    from config.env_loader import be_context
    from db.db_connector import SessionLocal
    db = SessionLocal()
    with be_context():
        from app.models.document import Document
        from app.models.document import DocumentChunk, DocumentSummary

        all_docs = db.query(Document).all()
        print(f"총 {len(all_docs)}개의 문서가 발견됨")

        for doc in tqdm(all_docs, desc="Summary Backfill 진행 중"):
            chunks = db.query(DocumentChunk).filter_by(document_id=doc.id).all()
            if not chunks:
                continue

            update_all_summaries(db, doc, chunks, DocumentSummary)
            db.commit()

    db.close()
    return {
        "status": "summary backfill completed",
    }