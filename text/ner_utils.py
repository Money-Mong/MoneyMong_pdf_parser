# text/ner_utils.py

import os
import re
import pandas as pd
import numpy as np
from collections import defaultdict

# 한국 상장 기업 사전
CSV_PATH = os.path.join("resource", "KRX_company.csv")

def load_company_data():
    df = pd.read_csv(CSV_PATH)

    # 정규화된 기업명
    df["norm_name"] = df["company_name_kr"].apply(
        lambda x: x.replace(" ", "").replace("(주)", "").strip()
    )

    # alias 리스트 정리 (한글명, 영문명)
    df["alias_list"] = df["aliases"].fillna("").apply(
        lambda x: [
            a.replace(" ", "").replace("(주)", "").strip()
            for a in x.split(",")
        ]
    )

    return df


COMPANY_DF = load_company_data()


# 이름/alias → ticker & industry 매핑  기업명 → {ticker, industry}
COMPANY_MAP = {}  

for _, row in COMPANY_DF.iterrows():

    COMPANY_MAP[row["norm_name"]] = {
        "ticker": row["ticker"],
        "industry": row["industry"]
    }

    for al in row["alias_list"]:
        if al:
            COMPANY_MAP[al] = {
                "ticker": row["ticker"],
                "industry": row["industry"]
            }

def normalize_company(name: str) -> str:
    return name.replace(" ", "").replace("(주)", "").strip()



def map_to_company(entity: str):
    """
    NER 엔티티(OG)를 실제 상장기업 ticker + industry 로 매핑
    """
    norm = normalize_company(entity)

    # 완전 일치
    if norm in COMPANY_MAP:
        return norm, COMPANY_MAP[norm]["ticker"], COMPANY_MAP[norm]["industry"]

    # 부분 일치
    for name_key, info in COMPANY_MAP.items():
        if name_key in norm or norm in name_key:
            return name_key, info["ticker"], info["industry"]

    return None, None, None



def aggregate_entities(ner_results):
    stats = defaultdict(lambda: {"freq": 0, "scores": []})

    for ent in ner_results:
        if ent["entity_group"] not in ["ORG", "OG"]:
            continue

        name = ent["word"]
        score = float(ent["score"])

        stats[name]["freq"] += 1
        stats[name]["scores"].append(score)

    # 평균 score 계산
    for name, v in stats.items():
        v["avg_score"] = sum(v["scores"]) / len(v["scores"])

    return stats


def aggregate_entities_extended(ner_results):
    ents = defaultdict(list)

    for ent in ner_results:
        ents[ent["entity_group"]].append({
            "text": ent["word"],
            "score": float(ent["score"])
        })

    return ents


def is_invalid_keyword(kw: str) -> bool:
    kw = kw.strip()

    if re.fullmatch(r"\d+", kw): return True
    if re.fullmatch(r"\d+\s*\)", kw): return True
    if re.fullmatch(r"\d{2,4}년", kw): return True
    if re.fullmatch(r"\d{4}", kw): return True
    if re.fullmatch(r"\d{1,2}\.\d{1,2}", kw): return True

    if "%" in kw: return True
    if "원" in kw: return True
    if "억원" in kw: return True
    if "달러" in kw: return True

    if kw.startswith("##"): return True

    # 6자리 숫자(티커)
    if re.fullmatch(r"\d{6}", kw):
        return True

    # 기업명은 keyword에서 제외
    if normalize_company(kw) in COMPANY_MAP:
        return True

    return False



# 키워드 생성 함수
def build_keywords_from_entities(entities):
    keywords = set()

    for label, items in entities.items():
        for ent in items:
            kw = ent["text"].strip()

            if len(kw) <= 1:
                continue

            if is_invalid_keyword(kw):
                continue

            keywords.add(kw)

    return list(keywords)



def compute_company_scores(stats, alpha=2.0):
    scored = []

    for name, v in stats.items():
        avg = float(v["avg_score"])
        final_score = float(v["freq"] + avg * alpha)

        scored.append({
            "name": name,
            "freq": int(v["freq"]),
            "avg_score": avg,
            "score": final_score,
        })

    return sorted(scored, key=lambda x: -x["score"])
