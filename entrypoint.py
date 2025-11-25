import runpod

def handler(event):
    try:
        print("=== HANDLER STARTED ===")
        
        # 모듈 임포트 시도
        try:
            from app.services.pipeline.pipeline_db_store import run_db_store_pipeline
            print("✅ Successfully imported run_db_store_pipeline")
        except Exception as import_err:
            print(f"❌ Import Error: {import_err}")
            return {
                "status": "error",
                "message": f"Import failed: {str(import_err)}"
            }

        run_db_store_pipeline()
        print("✅ Pipeline completed")

        return {
            "status": "completed",
            "message": "PDFs parsed and stored."
        }

    except Exception as e:
        print(f"❌ ERROR in handler: {str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }

if __name__ == "__main__":
    print("🚀 Entrypoint started")
    runpod.serverless.start({"handler": handler})
