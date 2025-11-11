def build_document_json(result):
    report_id = result["document_id"]
    
    # chunks (임베딩 포함)
    chunks = [
        {
            "chunk_id": c["chunk_index"],
            "content": c["content"],
            "embedding": c["embedding"],
            "page": c["page_numbers"][0]
        }
        for c in result["chunk_records"]
    ]

    # non-text blocks (표/이미지 등)
    non_text_blocks = [
        {
            "content_type": a["asset_type"],
            "bbox_pdf": a["metadata"]["bbox_pdf"],
            "bbox_image": a["metadata"]["bbox_image"],
            "image_path": a["file_path"],
            "page": a["page_number"]
        }
        for a in result["asset_records"]
    ]

    doc_to_json = {
        "document_id": report_id,
        "chunks": chunks,
        "non_text_blocks": non_text_blocks
    }

    return doc_to_json