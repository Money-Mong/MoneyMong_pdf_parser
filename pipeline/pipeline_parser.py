import os, json
import boto3
from datetime import datetime
from layout.save_page import save_first_page
from layout.detect_table_crop import detect_table_crop
from layout.detect_layout import detect_layout
from text.pdfminer_extractor import extract_text
from text.text_cleaner import clean_text
from text.embedding import chunk_and_embed
from utils.file_loader import get_local_pdf_files
from utils.file_io import save_json

def run_pdf_pipeline():
    processed = []
    all_results = []
    
    pdf_files = get_local_pdf_files()                                                                   # s3 > 로컬 > 로컬와 s3key 반환                                                           
    for original_name, local_pdf_path in pdf_files:
        report_id = os.path.splitext(os.path.basename(original_name))[0]

        print(f"📄 Processing {report_id}...")

        try:
        # pdf to img
            page_img = save_first_page(local_pdf_path, report_id)
            
            # layout detect : layout_records
            layout_elements = detect_layout(page_img, report_id=report_id)
            
            # table crop : asset_records
            table_layout_boxes = detect_table_crop(page_img, report_id=report_id)
            
            # text 추출
            text = extract_text(pdf_path=local_pdf_path, layout_boxes=table_layout_boxes)
            if len(text) < 50 :
                continue
            clean = clean_text(text)
            
            # 텍스트에 대한 chunk, embedding : chunk_records
            chunk_records = chunk_and_embed(text=clean, report_id=report_id)

            # 전체 모듈에 대한 반환 확인
            result = {
                "document_id":report_id,
                "layout_records":layout_elements,
                "asset_records":table_layout_boxes,
                "chunk_records":chunk_records,
                "created_at": datetime.utcnow().isoformat()
                }
            all_results.append(result)
            processed.append(report_id)

        except Exception as e:
            print(f"❌ Error processing {report_id}: {e}")
            continue

    return processed, all_results


