# MoneMong_pdf_parser/db/insert_chunk.py

def insert_chunks(db, DocumentChunk, document_id, chunk_records):
    """텍스트 청크 삽입"""
    for rec in chunk_records:
        chunk = DocumentChunk(
            document_id=document_id,
            chunk_index=rec["chunk_index"],
            content=rec["content"],
            content_type=rec["content_type"],
            page_numbers=rec["page_numbers"],
            embedding=rec["embedding"],
            keywords=rec["keywords"],
            chunk_metadata=rec["metadata"],
            token_count=rec["token_count"],
            created_at=rec["created_at"]
        )
        db.add(chunk)
    print(f"🧩 Chunks inserted: {len(chunk_records)} records")
