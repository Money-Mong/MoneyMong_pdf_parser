# MoneMong_pdf_parser/db/insert_document.py

from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
import os

def insert_or_update_document(db: Session, Document, result, pdf_path=None, mode="update"):

    report_id = result["document_id"]
    file_size = os.path.getsize(pdf_path) if pdf_path and os.path.exists(pdf_path) else None

    if mode == "update":
        try:
            # source_nid = report_id 로 기존 문서 찾기
            doc = db.query(Document).filter_by(source_nid=report_id).one()

            # 기존 문서의 메타데이터 갱신 (pending->completed)
            doc.processing_status = "completed"
            doc.file_path = pdf_path
            doc.file_size = file_size
            db.flush()

            print(f"🟢 Updated existing document: {report_id} (uuid={doc.id})")
            return doc
        
        except NoResultFound:
            print(f"⚠️ No document found for report_id={report_id}, creating new one...")
            mode = "create"

    if mode == "create":
        doc = Document(
            source_type="pdf",
            source_url=None,
            source_nid=report_id,
            title=report_id,
            author="PDF Parser",
            file_path=pdf_path,
            file_size=file_size,
            language="ko",
            processing_status="completed",
        )
        
        db.add(doc)
        db.flush()
        print(f"📄 Created new document: {report_id} (uuid={doc.id})")
        return doc
