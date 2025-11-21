from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

MODEL_NAME = "soddokayo/klue-roberta-large-klue-ner"

_ner_pipeline = None  # 전역 변수로 pipeline 저장


def get_ner_pipeline():
    global _ner_pipeline

    if _ner_pipeline is None:
        print("🔁 Loading NER model...")
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model = AutoModelForTokenClassification.from_pretrained(MODEL_NAME)
        _ner_pipeline = pipeline(
            "ner",
            model=model,
            tokenizer=tokenizer,
            aggregation_strategy="simple"
        )
        print("✅ NER model loaded.")

    return _ner_pipeline