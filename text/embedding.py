from langchain_upstage import UpstageEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os
from datetime import datetime

# .env 파일 로드
load_dotenv()

# Upstage API 키 로드
api_key = os.getenv("UPSTAGE_API_KEY")

# LangChain Upstage 임베딩 모델 초기화
embedding_model = UpstageEmbeddings(
    model="embedding-passage",
    api_key=api_key
    
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


# from langchain_openai import OpenAIEmbeddings
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from config.env_loader import OPENAI_API_KEY

# def chunk_and_embed(text, chunk_size=500, overlap=100):
#     splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
#     chunks = splitter.split_text(text)
#     embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=OPENAI_API_KEY)
#     embeds = embeddings.embed_documents(chunks)
#     return [{"chunk_id":i+1, "content":c, "embedding":e} for i,(c,e) in enumerate(zip(chunks, embeds))]
