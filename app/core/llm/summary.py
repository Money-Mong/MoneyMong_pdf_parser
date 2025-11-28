# core/llm/summary.py
import os
import json
from langchain_core.prompts import PromptTemplate
from app.core.llm.llm import get_summary_llm
from app.core.text.ner import extract_summary_entities
from app.core.llm.prompts import SUMMARY_PROMPT

def doc_summary(full_text: str):

    llm = get_summary_llm()

    prompt = PromptTemplate(
        template=SUMMARY_PROMPT,
        input_variables=["report_content"],
    )

    chain = prompt | llm
    result = chain.invoke({"report_content": full_text})
    raw_output = result.content

    try:
        summary_data = json.loads(raw_output)
    except:
        # 모델이 XML 또는 text로 줄 경우 예외 처리
        summary_data = {
            "summary_short": raw_output[:200],
            "summary_long": raw_output[:1000],
            "key_points": [],
            "entities": {},
        }

    ner_entities = extract_summary_entities(full_text)


    summary_data["entities"] = ner_entities
    summary_data["model_version"] = "upstage_chatupstage_solorpro2"

    return summary_data