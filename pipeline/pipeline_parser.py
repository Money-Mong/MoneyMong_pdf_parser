# pipeline/pipeline_parser.py
import os
from datetime import datetime

from layout.save_page import save_first_page
from layout.detect_table_crop import detect_table_crop
from layout.detect_layout import detect_layout
from text.pdfminer_extractor import extract_text
from text.text_cleaner import clean_text
from text.embedding import chunk_and_embed

"""단일 PDF 파일 파싱 → layout / asset / chunk 추출"""

def parse_single_pdf(report_id, local_pdf_path):
    print(f"📄 Parsing {report_id}...")

    try:
        # 첫 페이지 이미지 변환
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

        clean = clean_text(text)

        # 5) 청크 & 임베딩
        chunk_records = chunk_and_embed(clean, report_id)

        return {
            "report_id": report_id,
            "layout_records": layout_elements,
            "asset_records": table_layout_boxes,
            "chunk_records": chunk_records,
            "created_at": datetime.utcnow().isoformat(),
        }

    except Exception as e:
        print(f"❌ Error parsing {report_id}: {e}")
        return None


