from app.core.text.ner import extract_main_company, ner_in_chunks
from app.utils.sanitize import sanitize_metadata

def doc_metadata(text_clean):
        
    ner_results = ner_in_chunks(text_clean)
    company_info = extract_main_company(ner_results)

    main_company = company_info["main_company"]
    main_ticker = company_info["main_ticker"]
    company_scores = company_info["company_scores"]
    company_industry = company_info['industry']

    doc_metadata = {
        "main_company": main_company,
        "main_ticker": main_ticker,
        "industry" : company_industry,
        "company_scores": company_scores
    }

    doc_metadata = sanitize_metadata(doc_metadata)
    
    return doc_metadata