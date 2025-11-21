# services/pipeline/ner_backfill.py
# services/pipeline/ner_backfill.py
from app.core.text.model_loader import get_ner_pipeline
from app.utils.sanitize import sanitize_metadata
from app.core.text.ner import ner_in_chunks, extract_main_company
from app.core.text.ner_utils import (
    map_to_company,
    aggregate_entities_extended,
    build_keywords_from_entities
)
from app.db.database import SessionLocal
from app.db.models.document import Document
from app.db.models.document import DocumentChunk
from sqlalchemy.orm import Session
from tqdm import tqdm

# -------------------------
# 문서-level 업데이트 함수
# -------------------------

def run_ner_backfill():
    
    db = SessionLocal()
    
    all_docs = db.query(Document).all()
    print(f"➡ 총 {len(all_docs)}개의 문서가 발견됨")

    

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


    # -------------------------
    # 청크-level 업데이트 함수
    # -------------------------

    def update_chunk_metadata(chunk, representative_company: str):
        ner_pipeline = get_ner_pipeline()
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

        # 엔티티 확장
        chunk_entities = aggregate_entities_extended(ner_results)

        # chunk 키워드 추출
        chunk_keywords = build_keywords_from_entities(chunk_entities)
        chunk.keywords = chunk_keywords

        # 메타데이터 저장
        chunk_metadata = {
            "chunk_orgs": chunk_orgs,
            "chunk_entities": chunk_entities,
            "main_company": representative_company   # 문서 레벨 대표기업
        }

        chunk.chunk_metadata = sanitize_metadata(chunk_metadata)


    for doc in tqdm(all_docs, desc="NER Backfill 진행 중"):
        chunks = db.query(DocumentChunk).filter_by(document_id=doc.id).all()
        if not chunks:
            continue

        # 문서 level
        update_document_metadata(db, doc, chunks)

        representative_company = doc.doc_metadata.get("main_company")

        # 청크 level
        for chunk in chunks:
            update_chunk_metadata(chunk, representative_company)

        db.commit()

    db.close()
    print("\n🎉 NER backfill completed!")

