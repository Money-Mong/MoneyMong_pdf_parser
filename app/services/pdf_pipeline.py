from pipeline.pipeline_db_store import run_db_store_pipeline

def process_all_pdfs():
    run_db_store_pipeline()
    return {"status": "completed", "message": "All PDF files processed."}
