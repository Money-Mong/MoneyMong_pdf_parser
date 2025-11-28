import runpod
import os
import sys

# ====== 필수 PATH 설정 (RunPod Serverless 표준) ======
ROOT = "/app"
APP_ROOT = "/app/app"

sys.path.insert(0, ROOT)
sys.path.insert(0, APP_ROOT)

print("🔍 MAIN.PY LOADED")
print("📁 CWD:", os.getcwd())
print("📁 ROOT:", ROOT)
print("📁 File list:", os.listdir(ROOT))
print("📁 PYTHONPATH:", sys.path)


# ====== handler 함수 (RunPod Serverless 공식 포맷) ======
def handler(job):
    """
    job = {
        'id': '123',
        'input': { ... }
    }
    """

    print("🔥 Raw Job:", job)

    # 입력 검증
    if "input" not in job:
        return {"error": "Missing 'input' field"}

    # ====== pipeline import ======
    try:
        from app.services.pipeline.pipeline_db_store import run_db_store_pipeline
        print("📦 Import Success: run_db_store_pipeline")
    except Exception as e:
        print("❌ Import Error:", e)
        return {"error": f"import failed: {e}"}

    # ====== pipeline 실행 ======
    try:
        print("🚀 Running pipeline...")
        run_db_store_pipeline()
        print("🎉 Pipeline Completed")
        return {"status": "completed"}
    except Exception as e:
        print("❌ Pipeline Error:", e)
        return {"error": f"pipeline failed: {e}"}


# ====== RunPod Serverless 시작 ======
if __name__ == "__main__":
    print("🚀 Starting Runpod Serverless Worker...")
    try:
        runpod.serverless.start({"handler": handler})
    except Exception as server_err:
        print("❌ runpod.serverless.start() FAILED:", server_err)
