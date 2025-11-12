# from langchain_openai import OpenAIEmbeddings
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

def chunk_and_embed(text, report_id, page_number=1, chunk_size=500, overlap=100):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        length_function=len
    )
    chunks = splitter.split_text(text)

    embeddings = embedding_model.embed_documents(chunks)
    now = datetime.utcnow().isoformat()

    return [
        {
            "document_id": report_id,
            "chunk_index": i + 1,
            "content": c,
            "content_type": "text",
            "page_numbers": [page_number],
            "embedding": e,
            "keywords": [],
            "metadata": {},
            "token_count": len(c.split()),
            "created_at": now
        }
        for i, (c, e) in enumerate(zip(chunks, embeddings))
    ]
