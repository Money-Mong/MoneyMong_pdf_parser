from sqlalchemy.orm import Session
from app.models.document import Document

# processing_status==pending인 문서만 조회
def get_pending_documents(db: Session):
    return db.query(Document).filter(Document.processing_status == "pending").all()
