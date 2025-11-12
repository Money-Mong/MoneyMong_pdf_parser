# MoneMong_pdf_parser/db/insert_asset.py

def insert_assets(db, DocumentAsset, document_id, asset_records):
    """자산(표/이미지 등) 데이터 삽입"""
    for rec in asset_records:
        asset = DocumentAsset(
            document_id=document_id,
            asset_type=rec["asset_type"],
            page_number=rec["page_number"],
            file_path=rec["file_path"],
            raw_data=rec.get("raw_data"),
            description=rec.get("description"),
            extracted_text=rec.get("extracted_text"),
            asset_metadata=rec["metadata"],
            created_at=rec["created_at"]
        )
        db.add(asset)
    print(f"🖼️ Assets inserted: {len(asset_records)} records")
