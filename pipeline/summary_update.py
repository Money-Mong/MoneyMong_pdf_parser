# pipeline/pipeline_summary.py
import os
from config.paths import S3_BUCKET
from utils.file_loader import download_s3_pdf_to_temp
from text.pdfminer_extractor import extract_text
from text.text_cleaner import clean_text
from summary.doc_summary import doc_summary
from db.insert_summary import insert_summary


def update_document_summary(db, Document, DocumentSummary, document):
    """
    이미 completed 상태인 문서라도 summary만 재생성하여 업데이트
    """

    try:
        # 1) S3 경로 확보
        s3_path = document.file_path
        s3_key = s3_path.replace(f"s3://{S3_BUCKET}/", "")

        # 2) 로컬 다운로드
        local_pdf_path = download_s3_pdf_to_temp(S3_BUCKET, s3_key)

        # 3) 텍스트 추출 (첫 페이지/레이아웃은 사용 X → 전체 페이지 추출)
        text = extract_text(pdf_path=local_pdf_path, layout_boxes=None)
        text_clean = clean_text(text)

        # 4) 요약 생성
        summary_data = doc_summary(text_clean)

        # 5) summary DB 삽입/업데이트
        summary_id = insert_summary(
            db, DocumentSummary,
            document_id=document.id,
            summary=summary_data
        )

        db.commit()
        print(f"✅ Summary updated for document {document.id} (summary_id={summary_id})")

    except Exception as e:
        print(f"❌ Error updating summary for {document.id}: {e}")
