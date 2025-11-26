import runpod

def handler(event):
    print("🔥 Raw Event:", event)

    if not event or "input" not in event:
        return {"status": "error", "message": "Missing 'input' in event"}

    print("=== event succes, HANDLER STARTED ===")

    # Import test
    try:
        from app.services.pipeline.pipeline_db_store import run_db_store_pipeline
        print("✅ run_db_store_pipeline import success")
    except Exception as e:
        print("❌ Import Error:", e)
        return {"status": "error", "message": f"Import failed: {str(e)}"}

    try:
        print("🚀 Running pipeline...")
        run_db_store_pipeline()
        print("🎉 Pipeline completed")
        return {"status": "completed"}
    except Exception as e:
        print("❌ Pipeline Error:", str(e))
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    print("🚀 Entrypoint started")
    runpod.serverless.start({"handler": handler})