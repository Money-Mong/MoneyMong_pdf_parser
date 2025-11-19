# utils/ner_loader.py

from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

MODEL_NAME = "soddokayo/klue-roberta-large-klue-ner"
print(f"Loading NER model")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForTokenClassification.from_pretrained(MODEL_NAME)

ner_pipeline = pipeline(
    "ner",
    model=model,
    tokenizer=tokenizer,
    aggregation_strategy="simple"
)

print("✅ NER model loaded.")
