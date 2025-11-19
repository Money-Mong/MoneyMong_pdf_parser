# pipeline_db_store.py
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.db_connector import SessionLocal
from utils.file_loader import download_s3_pdf_to_temp
from db.queries import get_pending_documents
from pipeline.pipeline_parser import parse_single_pdf
from db.insert_pipeline import insert_pipeline_result
from config.env_loader import be_context
from config.paths import S3_BUCKET


def run_db_store_pipeline():

    db = SessionLocal()

    with be_context():
        from app.models.document import Document
        from app.models.document import DocumentLayout, DocumentAsset, DocumentChunk, DocumentSummary

        # DB pending 문서 조회
        pending_docs = get_pending_documents(db, Document)
        print(f"📄 Found {len(pending_docs)} pending documents in DB.")

        for doc in pending_docs:
            try:
                print(f"\n🚀 Processing: {doc.id}")

                # File_path → S3 key 변환
                s3_path = doc.file_path
                s3_key = s3_path.replace(f"s3://{S3_BUCKET}/", "")

                print(f"📥 S3 key = {s3_key}")

                # S3 → 로컬 PDF 다운로드
                local_pdf_path = download_s3_pdf_to_temp(S3_BUCKET, s3_key)

                # 파싱 수행
                result = parse_single_pdf(
                    report_id=doc.source_nid,     
                    local_pdf_path=local_pdf_path
                )

                if not result:
                    print(f"⚠️ Parsing failed for {doc.id}, marking as failed...")
                    doc.processing_status = "failed"
                    db.commit()
                    continue

                # DB 저장 (document.id → FK)
                insert_pipeline_result(
                    result,
                    db,
                    Document, DocumentLayout, DocumentAsset, DocumentChunk, DocumentSummary,
                    pdf_path=s3_key
                )

                # 문서 상태 업데이트
                doc.processing_status = "completed"
                db.commit()

                print(f"✅ Completed: {doc.id}")

            except Exception as e:
                print(f"❌ Error processing {doc.id}: {e}")
                doc.processing_status = "failed"
                db.commit()
                continue

    db.close()
    print("\nAll pending documents processed.")


