from app.services.pipeline.pipeline_db_store import run_db_store_pipeline

def handler(event):
    run_db_store_pipeline()
    return {
        "status": "completed",
        "message": "PDFs parsed and stored."
    }