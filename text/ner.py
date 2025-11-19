# text/doc_ner.py
from utils.ner_loader import ner_pipeline
from text.ner_utils import (
    aggregate_entities, compute_company_scores, map_to_company,
    aggregate_entities_extended, build_keywords_from_entities
)

def extract_main_company(ner_results):

    print("...Extracting main company from NER results...")

    # 엔티티 집계
    stats = aggregate_entities(ner_results)

    if not stats:
        return {
            "main_company": None,
            "main_ticker": None,
            "industry": None,
            "company_scores": [],
            "entities": aggregate_entities_extended(ner_results),
            "keywords": []
        }

    # 기업별 점수 계산
    scored = compute_company_scores(stats)

    best_name = scored[0]["name"]

    # CSV 기반 기업 매핑 (기업명, ticker, industry)
    mapped_name, ticker, industry = map_to_company(best_name)

    # 전체 엔티티
    entities = aggregate_entities_extended(ner_results)

    # 키워드
    keywords = build_keywords_from_entities(entities)

    return {
        "main_company": mapped_name,
        "main_ticker": ticker,
        "industry": industry,
        "company_scores": scored,
        "entities": entities,
        "keywords": keywords
    }


def ner_in_chunks(text, max_length=512):

    chunk_size = 400
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

    all_results = []

    for ch in chunks:
        res = ner_pipeline(ch)
        all_results.extend(res)

    return all_results