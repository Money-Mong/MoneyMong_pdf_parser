from app.services.pipeline.pipeline_db_store import run_db_store_pipeline

def handler(event):
    run_db_store_pipeline()
    print('process진입')
    return {
        "status": "completed",
        "message": "PDFs parsed and stored."
    }