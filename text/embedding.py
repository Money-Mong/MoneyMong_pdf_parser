# from langchain_openai import OpenAIEmbeddings
from utils.ner_loader import ner_pipeline
from text.ner_utils import map_to_company, aggregate_entities_extended, build_keywords_from_entities
from langchain_community.embeddings import HuggingFaceEmbeddings
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
        ner_results = ner_pipeline(chunk)

        # ORG 개체명 수집
        chunk_orgs = []
        for e in ner_results:
            if e["entity_group"] == "ORG":
                mapped, ticker = map_to_company(e["word"])
                if mapped:
                    chunk_orgs.append({
                        "name": mapped,
                        "ticker": ticker,
                        "score": e["score"]
                    })

        # chunk keywords 생성
        chunk_entities = aggregate_entities_extended(ner_results)
        chunk_keywords = build_keywords_from_entities(chunk_entities)

        records.append({
            "report_id": report_id,
            "chunk_index": i + 1,
            "content": chunk,
            "content_type": "text",
            "page_numbers": [page_number],
            "embedding": emb,
            "keywords": chunk_keywords,  # 🔥 chunk-level keywords
            "metadata": {
                "chunk_orgs": chunk_orgs,
                "representative_company": representative_company
            },
            "token_count": len(chunk.split()),
            "created_at": now
        })

    return records