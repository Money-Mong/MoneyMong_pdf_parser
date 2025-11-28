# text/ner.py
from collections import defaultdict
from app.core.text.model_loader import get_ner_pipeline
from app.core.text.ner_utils import (
    aggregate_entities, compute_company_scores, map_to_company,
    aggregate_entities_extended, build_keywords_from_entities, normalize_company
)

'''NER OG 기반 main_company 추출'''
def extract_main_company(ner_results):
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



'''청크 레벨 NER'''
def ner_in_chunks(text, max_length=512):
    ner_pipeline = get_ner_pipeline()
    chunk_size = 400
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

    all_results = []

    for ch in chunks:
        res = ner_pipeline(ch)
        all_results.extend(res)

    return all_results


'''요약용 문서 레벨 NER'''
def extract_summary_entities(full_text: str):
    ner_pipeline = get_ner_pipeline()
    ner_results = ner_pipeline(full_text)

    company_counts = defaultdict(int)
    tickers = set()

    for ent in ner_results:
        if ent["entity_group"] in ["ORG", "OG"]:
            name = ent["word"]
            mapped, ticker, _ = map_to_company(name)
            if mapped:
                company_counts[mapped] += 1
                tickers.add(ticker)

    # 대표 기업 선정
    if company_counts:
        main_company = max(company_counts, key=company_counts.get)
        _, main_ticker, _ = map_to_company(main_company)
    else:
        main_company = None
        main_ticker = None

    key_figures = []

    for ent in ner_results:
        if ent["entity_group"] != "DT":
            continue

        val = ent["word"]

        # 숫자 판단 규칙
        if any(x in val for x in ["억", "조", "%"]):  # 매출/이익/성장률 가능성
            figure_type = "수치"

            if "%" in val:
                figure_type = "성장률"
            elif "억" in val or "조" in val:
                figure_type = "금액"

            key_figures.append({
                "value": val,
                "type": figure_type
            })

    # 상위 5개만 사용
    key_figures = key_figures[:5]

    extended = aggregate_entities_extended(ner_results)
    keywords = build_keywords_from_entities(extended)

    # 상위 10개만
    keywords = keywords[:10]

    return {
        "main_company": main_company,
        "main_ticker": main_ticker,
        "tickers": list(tickers),
        "key_figures": key_figures,
        "keywords": keywords
    }