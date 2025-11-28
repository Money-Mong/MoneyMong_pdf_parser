# app/services/task_service.py

from app.db.database import SessionLocal
from app.db.models.document import DocumentTask
from datetime import datetime
import requests
from app.config.settings import get_settings  # 필요 시

settings = get_settings()

def save_task_status(db, task_id, status, error_message=None):
    task = db.query(DocumentTask).filter_by(task_id=task_id).first()
    if not task:
        task = DocumentTask(
            task_id=task_id,
            status=status,
            error_message=error_message,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(task)
    else:
        task.status = status
        task.error_message = error_message
        task.updated_at = datetime.utcnow()
    db.commit()

def run_pipeline_with_lambda_notify(task_id):
    db = SessionLocal()
    try:
        save_task_status(db, task_id, "processing")
        from app.services.pipeline.pipeline_db_store import run_db_store_pipeline
        run_db_store_pipeline()
        save_task_status(db, task_id, "completed")
        
        requests.post(settings.LAMBDA_NOTIFY_URL, json={
            "task_id": task_id,
            "status": "completed"
        })

    except Exception as e:
        save_task_status(db, task_id, "failed", error_message=str(e))

        requests.post(settings.LAMBDA_NOTIFY_URL, json={
            "task_id": task_id,
            "status": "failed",
            "error": str(e)
        })
    finally:
        db.close()

def get_task_status_by_id(task_id: str):
    db = SessionLocal()
    try:
        task = db.query(DocumentTask).filter_by(task_id=task_id).first()
        if not task:
            return {"status": "not_found"}
        return {
            "task_id": task.task_id,
            "status": task.status,
            "error": task.error_message,
            "updated_at": task.updated_at.isoformat()
        }
    finally:
        db.close()
