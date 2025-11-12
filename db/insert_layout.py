# MoneMong_pdf_parser/db/insert_layout.py

def insert_layouts(db, DocumentLayout, document_id, layout_records):
    """레이아웃 요소 삽입"""
    for rec in layout_records:
        layout = DocumentLayout(
            document_id=document_id,
            page_number=rec["page_number"],
            element_type=rec["element_type"],
            element_order=rec["element_order"],
            bbox=rec["bbox"],
            content=rec.get("content"),
            asset_id=None,
            layout_metadata=rec["metadata"],
            created_at=rec["created_at"]
        )
        db.add(layout)
    print(f"📐 Layouts inserted: {len(layout_records)} records")
