from tqdm import tqdm
from fastapi import APIRouter
from app.services.pipeline.pipeline_db_store import run_db_store_pipeline

from app.db.database import SessionLocal
from app.db.models.document import Document, DocumentChunk, DocumentSummary
from app.services.summary_update import update_all_summaries
from app.services.ner_backfill import run_ner_backfill

router = APIRouter()

@router.get("/")
def root():
    return {"status": "ok", "message": "Moneymong S3 PDF Pipeline"}


@router.post("/pdf-processing")
def run_task():
    run_db_store_pipeline()
    return {
        "status": "completed",
        "message": "All PDF files processed and stored successfully."
    }


@router.post("/ner-backfill")
def ner_backfill_task():
    """
    기존에 DB에 쌓인 documents & document_chunks에 대해
    NER 기반 metadata / keywords를 채워 넣는 백필 작업
    """
    run_ner_backfill()
    return {
        "status": "completed",
        "message": "NER backfill executed successfully.",
    }


@router.post("/summary-backfill")
def summary_bakfill_tast():
    """
    기존에 DB에 쌓인 documents 에 대해
    document_summary 채워 넣는 백필 작업
    """
    db = SessionLocal()

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