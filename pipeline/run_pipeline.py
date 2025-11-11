import os, json
from datetime import datetime
from config.paths import PDF_FOLDER, JSON_DIR
from layout.save_page import save_first_page
from layout.detect_table_crop import detect_table_crop
from layout.detect_layout import detect_layout
from text.pdfminer_extractor import extract_text
from text.text_cleaner import clean_text
from text.embedding import chunk_and_embed
from utils.file_io import save_json

def run_pipeline():
    pdf_files = [f for f in os.listdir(PDF_FOLDER) if f.endswith('.pdf')]
    processed = []
    all_results = []
    for f in pdf_files:
        report_id = os.path.splitext(f)[0]
        pdf_path = os.path.join(PDF_FOLDER, f)

        # pdf to img
        page_img = save_first_page(pdf_path, report_id)
        
        # layout detect : layout_records
        layout_elements = detect_layout(page_img_path= page_img, report_id=report_id)
        
        # table crop : asset_records
        table_layout_boxes = detect_table_crop(page_img_path= page_img, report_id=report_id)
        
        # text 추출
        text = extract_text(pdf_path=pdf_path, layout_boxes=table_layout_boxes)
        if len(text) < 50 : continue
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
        
        # print(result) # test용
        # json_path = os.path.join(JSON_DIR, f"{report_id}.json")
        # save_json(result, json_path)
        processed.append(report_id)
    return processed, all_results


# def run_pipeline():
#     pdf_files = [f for f in os.listdir(PDF_FOLDER) if f.endswith('.pdf')]
#     processed = []
#     for f in pdf_files:
#         report_id = os.path.splitext(f)[0]
#         pdf_path = os.path.join(PDF_FOLDER, f)
#         page_img = save_first_page(pdf_path, report_id)
#         table_layout_boxes = detect_table_crop(page_img, report_id)
#         text = extract_text(pdf_path, table_layout_boxes)
#         if len(text) < 50 : continue
#         clean = clean_text(text)
#         chunks = chunk_and_embed(clean)
#         result = {"report_id":report_id,"chunks":chunks,"non_text_blocks":table_layout_boxes}
#         json_path = os.path.join(JSON_DIR, f"{report_id}.json")
#         save_json(result, json_path)
#         processed.append(report_id)
#     return processed
