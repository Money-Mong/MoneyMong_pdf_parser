print('entry 진입')
import runpod

def handler(event):
    print("=== HANDLER REACHED ===")
    return {
        "status": "success",
        "input_received": event.get('input', None)
    }

if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})


# import runpod
# from app.services.pipeline.pipeline_db_store import run_db_store_pipeline

# def handler(event):
#     try:
#         print("==== STARTING PDF PROCESSING ====")
#         run_db_store_pipeline()
#         print("==== COMPLETED PDF PROCESSING ====")
#         return {
#             "status": "completed",
#             "message": "PDFs parsed and stored."
#         }
#     except Exception as e:
#         print(f"ERROR in handler: {str(e)}")
#         return {
#             "status": "error",
#             "message": str(e)
#         }

# if __name__ == "__main__":
#     runpod.serverless.start({"handler": handler})
