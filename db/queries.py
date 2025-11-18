# db/queries.py
from sqlalchemy.orm import Session
from sqlalchemy import or_
def get_pending_documents(db: Session, Document):
    return db.query(Document).filter(
        or_(
            Document.processing_status == "pending",
            Document.processing_status == "failed"
        )
    ).all()