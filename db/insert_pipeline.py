import os, sys
from contextlib import contextmanager
from sqlalchemy.orm import Session
from db.insert_document import insert_or_update_document
from db.insert_layout import insert_layouts
from db.insert_asset import insert_assets
from db.insert_chunk import insert_chunks

"""
    파이프라인 결과를 DB에 삽입/갱신
    """

def insert_pipeline_result(result, db, Document, DocumentLayout, DocumentAsset, DocumentChunk, pdf_path=None):

    # document 업데이트 or 생성
    document = insert_or_update_document(db, Document, result, pdf_path=pdf_path, mode="update")

    # 하위 레코드들 삽입
    insert_layouts(db, DocumentLayout, document.id, result["layout_records"])
    insert_assets(db, DocumentAsset, document.id, result["asset_records"])
    insert_chunks(db, DocumentChunk, document.id, result["chunk_records"])

    db.commit()
    print(f"✅ Pipeline DB update completed for {result['document_id']} (uuid={document.id})")
    return document.id