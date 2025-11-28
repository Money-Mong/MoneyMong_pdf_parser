# pipeline/pipeline_parser.py
import os
from datetime import datetime

from app.core.layout.save_page import save_first_page
from app.core.layout.detect_table_crop import detect_table_crop
from app.core.layout.detect_layout import detect_layout
from app.core.text.pdfminer_extractor import extract_text
from app.core.text.text_cleaner import clean_text
from app.core.text.embedding import chunk_and_embed
from app.core.llm.summary import doc_summary
from app.services.metadata import doc_metadata

def parse_single_pdf(report_id, local_pdf_path):
    print(f"📄 Parsing {report_id}...")

    try:
        # 페이지 이미지 변환
        page_img = save_first_page(local_pdf_path, report_id)

        # 레이아웃 분석
        layout_elements = detect_layout(page_img, report_id=report_id)

        # 테이블 crop
        table_layout_boxes = detect_table_crop(page_img, report_id=report_id)

        # 텍스트 추출
        text = extract_text(pdf_path=local_pdf_path, layout_boxes=table_layout_boxes)
        if len(text) < 30:
            print(f"⚠️ Skipping {report_id}: text too short.")
            return None

        text_clean = clean_text(text)

        # 문서 요약
        summary_data = doc_summary(text_clean)
        
        # 문서 단위 metadata 구성
        doc_meta = doc_metadata(text_clean)
        print('❤️ 주 기업: ',doc_meta['main_company'])
        # 청크 & 임베딩
        chunk_records = chunk_and_embed(text_clean, report_id, representative_company=doc_meta['main_company'])

        return {
            "report_id": report_id,
            "layout_records": layout_elements,
            "asset_records": table_layout_boxes,
            "chunk_records": chunk_records,
            "document_metadata" : doc_meta,
            "document_summary" : summary_data,
            "created_at": datetime.utcnow().isoformat(),
        }

    except Exception as e:
        print(f"❌ Error parsing {report_id}: {e}")
        return None


