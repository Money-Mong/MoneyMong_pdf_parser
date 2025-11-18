# text/ner_korean.py

from utils.ner_loader import get_ner_pipeline

def extract_entities(text: str):
    ner = get_ner_pipeline()
    outputs = ner(text)

    entities = []
    for ent in outputs:
        entities.append({
            "text": ent["word"],
            "label": ent["entity_group"],   
            "score": float(ent["score"]),
        })
    return entities


def extract_stock_candidates(entities):

    orgs = {e["text"] for e in entities if e["label"] == "ORG"}
    return list(orgs)
