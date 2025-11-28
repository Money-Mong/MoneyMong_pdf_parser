# embedding.py
# from langchain_openai import OpenAIEmbeddings
from app.core.text.model_loader import get_ner_pipeline
from app.core.text.ner_utils import map_to_company, aggregate_entities_extended, build_keywords_from_entities
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os
from datetime import datetime

# .env 파일 로드
load_dotenv()
# api_key = os.getenv("OPENAI_API_KEY")
embedding_model = HuggingFaceEmbeddings(
    model_name="sangmini/msmarco-cotmae-MiniLM-L12_en-ko-ja",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True}
    )

'''청킹, 임베딩, 청크 레벨 NER 수행'''
def chunk_and_embed(text, report_id, representative_company=None,
                    page_number=1, chunk_size=500, overlap=100):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        length_function=len
    )
    chunks = splitter.split_text(text)
    embeddings = embedding_model.embed_documents(chunks)
    now = datetime.utcnow().isoformat()

    records = []

    for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
        # chunk-level NER
        ner_pipeline = get_ner_pipeline()
        ner_results = ner_pipeline(chunk)

        # OG 개체명 수집
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

        records.append({
            "report_id": report_id,
            "chunk_index": i + 1,
            "content": chunk,
            "content_type": "text",
            "page_numbers": [page_number],
            "embedding": emb,
            "keywords": chunk_keywords,  
            "chunk_metadata": {
                "chunk_orgs": chunk_orgs,
                "chunk_entities": chunk_entities,
                "main_company": representative_company
            },
            "token_count": len(chunk.split()),
            "created_at": now
        })

    return records