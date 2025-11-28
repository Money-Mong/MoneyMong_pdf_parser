import uuid
from tqdm import tqdm
from fastapi import APIRouter, BackgroundTasks
from app.services.pipeline.pipeline_db_store import run_db_store_pipeline

from app.db.database import SessionLocal
from app.db.models.document import Document, DocumentChunk, DocumentSummary
from app.services.summary_update import update_all_summaries
from app.services.ner_backfill import run_ner_backfill

router = APIRouter()
tasks = {}

@router.get("/")
def root():
    return {"status": "ok", "message": "Moneymong S3 PDF Pipeline"}

@router.post("/pdf-processing")
def process_pdf(background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())

    # 작업 등록
    background_tasks.add_task(run_pdf_parsing_task, task_id)

    # 즉시 응답
    return {"task_id": task_id, "status": "processing_started"}
# @router.post("/pdf-processing")
# def run_task():
#     run_db_store_pipeline()
#     return {
#         "status": "completed",
#         "message": "All PDF files processed and stored successfully."
#     }
def run_pdf_parsing_task(task_id):
    try:
        # 여기서 PDF 처리 로직 수행
        run_db_store_pipeline()

        # 작업 성공 결과 저장
        tasks[task_id] = {"status": "completed"}
    except Exception as e:
        tasks[task_id] = {"status": "failed", "error": str(e)}


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

@router.get("/pdf-status/{task_id}")
def get_status(task_id: str):
    if task_id not in tasks:
        return {"status": "not_found"}
    return tasks[task_id]


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