# MoneMong_pdf_parser/db/insert_document.py

from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
import os

def insert_or_update_document(db: Session, Document, result, pdf_path=None, mode="update"):

    report_id = result["report_id"]
    file_size = os.path.getsize(pdf_path) if pdf_path and os.path.exists(pdf_path) else None

    if mode == "update":
        try:
            # source_nid = report_id 로 기존 문서 찾기
            doc = db.query(Document).filter_by(source_nid=report_id).one()

            # 기존 문서 상태 갱신 
            doc.processing_status = "completed"

            db.flush()

            print(f"🟢 Updated existing document: {report_id} (uuid={doc.id})")
            return doc
        
        except NoResultFound:
            print(f"⚠️ No document found for report_id={report_id}, creating new one...")
            mode = "create"


    if mode == "create":

        existing_doc = (
            db.query(Document)
            .filter_by(source_nid=report_id)
            .order_by(Document.created_at.desc())
            .first()
        )

        if existing_doc and existing_doc.source_url:
            source_url = existing_doc.source_url
        else:
            raise ValueError(
                f"❌ source_url not found for report_id={report_id}. "
                f"PDF 파이프라인 전에 크롤링 단계에서 documents에 먼저 저장해야 합니다."
            )

        # 새로운 PDF 문서 생성
        doc = Document(
            source_type="pdf",
            source_url=source_url,   
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
