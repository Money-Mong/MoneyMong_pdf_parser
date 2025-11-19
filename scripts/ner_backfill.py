# scripts/ner_backfill.py

def run_ner_backfill():
    print("🔥 BE context activated. Importing models...")
    import sys
    # sys.path.insert(0, "/Users/jenzennii/Development/moneymong/MoneyMong_BE")
    # sys.path.insert(0, "/Users/jenzennii/Development/moneymong/MoneyMong_BE/app")

    
    from config.env_loader import be_context

    with be_context():   

        # BE 환경 기준 import
        from utils.sanitize import sanitize_metadata
        from text.ner import ner_in_chunks
        from db.db_connector import SessionLocal
        from app.models.document import Document,  DocumentChunk
        from utils.ner_loader import ner_pipeline
        from text.ner import extract_main_company
        from text.ner_utils import (
            map_to_company,
            aggregate_entities_extended,
            build_keywords_from_entities
        )
        from sqlalchemy.orm import Session
        from tqdm import tqdm


        db = SessionLocal()

        def update_document_metadata(db: Session, doc, chunks):
            full_text = "\n".join([c.content for c in chunks])
            
            ner_results = ner_in_chunks(full_text)
            company_info = extract_main_company(ner_results)

            main_company = company_info["main_company"]
            main_ticker = company_info["main_ticker"]
            company_scores = company_info["company_scores"]
            company_industry = company_info['industry']

            doc_metadata = {
                "main_company": main_company,
                "main_ticker": main_ticker,
                "industry" : company_industry,
                "company_scores": company_scores
            }
            doc_metadata = sanitize_metadata(doc_metadata)

            doc.doc_metadata = doc_metadata


        def update_chunk_metadata(chunk, representative_company: str):
            ner_results = ner_pipeline(chunk.content)

            # 청크 내부 기업 인식 정보
            chunk_orgs = []
            for e in ner_results:
                if e["entity_group"] == "OG":
                    mapped, ticker, _ = map_to_company(e["word"])
                    chunk_orgs.append({
                        "name": mapped if mapped else e["word"],
                        "ticker": ticker,
                        "score": float(e["score"])
                    })

            chunk_entities = aggregate_entities_extended(ner_results)

            # chunk 키워드 (chunk.keywords에 저장)
            chunk_keywords = build_keywords_from_entities(chunk_entities)
            chunk.keywords = chunk_keywords

            chunk_metadata = {
                "chunk_orgs": chunk_orgs,
                "chunk_entities": chunk_entities,
                "main_company": representative_company   # 문서 레벨 대표기업
            }

            chunk_metadata = sanitize_metadata(chunk_metadata)

            chunk.chunk_metadata = chunk_metadata


        print("📄 Loading all documents...")
        all_docs = db.query(Document).all()
        print(f"➡ 총 {len(all_docs)}개의 문서가 발견됨")

        for doc in tqdm(all_docs, desc="NER Backfill 진행 중"):
            chunks = db.query(DocumentChunk).filter_by(document_id=doc.id).all()
            if not chunks:
                continue

            update_document_metadata(db, doc, chunks)

            representative_company = doc.doc_metadata.get("main_company")

            for chunk in chunks:
                update_chunk_metadata(chunk, representative_company)

            db.commit()

        db.close()
        print("\n🎉 NER backfill completed!")

