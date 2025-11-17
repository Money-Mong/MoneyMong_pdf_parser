# MoneMong_pdf_parser/pipeline/pipeline_db_store.py
# run_pipeline의 반환값 → DB에 자동 삽입
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.env_loader import be_context
from db.db_connector import SessionLocal
from db.insert_pipeline import insert_pipeline_result
from pipeline.pipeline_parser import run_pdf_pipeline

""" PDF → 분석 → DB 저장 전체 프로세스"""

def run_db_store_pipeline():
    processed, all_results = run_pdf_pipeline()
    db = SessionLocal()

    # BE 환경에서 모델 import
    with be_context():
        from app.models.document import Document
        from app.models.document import DocumentLayout
        from app.models.document import DocumentAsset
        from app.models.document import DocumentChunk
        from config.paths import S3_BUCKET, S3_RAW_PREFIX

        for result in all_results:
            report_id = result["report_id"]

            # S3 경로
            pdf_path = f"s3://{S3_BUCKET}/{S3_RAW_PREFIX}{report_id}.pdf"

            print(f"🚀 Processing document: {report_id}")
            
            try:
                insert_pipeline_result(
                    result,
                    db,
                    Document, DocumentLayout, DocumentAsset, DocumentChunk,
                    pdf_path=pdf_path
                )
            except Exception as e:
                db.rollback()
                print(f"❌ Failed to insert {report_id}: {e}")
                continue
    
    db.close()
    print("🎉 All PDF documents processed and updated successfully.")
