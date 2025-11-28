# summary/update_summary_pipeline.py

from app.core.llm.summary import doc_summary   
from app.core.text.text_cleaner import clean_text

"""
    Document + chunks 기반 전체 summary 업데이트
    - 기존 summary 있으면 UPDATE
    - 없으면 CREATE
"""

def update_all_summaries(db, doc, chunks, DocumentSummary):

    full_text = "\n".join([c.content for c in chunks])
    if not full_text or len(full_text) < 20:
        print(f"⚠️ Skip summary: document {doc.id} has too little text")
        return None

    full_text_clean = clean_text(full_text)

    try:
        summary_data = doc_summary(full_text_clean)
    except Exception as e:
        print(f"❌ Error running summary LLM for {doc.id}: {e}")
        return None

    # 기존 summary 존재 여부 확인
    existing = db.query(DocumentSummary).filter_by(document_id=doc.id).first()

    if existing:
        '''--- UPDATE 모드 ---'''
        try:
            existing.summary_short = summary_data["summary_short"]
            existing.summary_long = summary_data["summary_long"]
            existing.key_points = summary_data.get("key_points", [])
            existing.entities = summary_data.get("entities", {})
            existing.model_version = summary_data.get("model_version", "unknown")
            db.flush()
            print(f"🔄 Updated summary for {doc.id}")
            return existing.id

        except Exception as e:
            print(f"❌ Error updating summary for {doc.id}: {e}")
            return None

    else:
        '''--- CREATE 모드 ---'''
        try:
            new_summary = DocumentSummary(
                document_id=doc.id,
                summary_short=summary_data["summary_short"],
                summary_long=summary_data["summary_long"],
                key_points=summary_data.get("key_points", []),
                entities=summary_data.get("entities", {}),
                model_version=summary_data.get("model_version", "unknown"),
            )
            db.add(new_summary)
            db.flush()
            print(f"🆕 Inserted new summary for {doc.id}")
            return new_summary.id

        except Exception as e:
            print(f"❌ Error inserting summary for {doc.id}: {e}")
            return None
